"""
Polymarket CLOB client wrapper.
Handles authentication, session management, and provides clean methods
for interacting with the orderbook and placing orders.

Upgraded:
  - Builder program integration for fee reductions
  - Batch orderbook fetching (500 tokens per call)
  - Batch order placement (up to 15 legs at once)
  - FOK/FAK market orders for guaranteed fills
  - GTD time-limited orders
  - Per-market fee rate lookup (most markets = 0% fee!)
  - Balance & allowance pre-checks
  - Heartbeat dead man's switch
  - Spread fetching for fast pre-filtering
  - Orderbook hash caching
  - Neg-risk market detection
"""

import logging
import time
import threading
from typing import Optional

import requests

from py_clob_client.client import ClobClient
from py_clob_client.clob_types import (
    OrderArgs,
    MarketOrderArgs,
    OrderType,
    BookParams,
    BalanceAllowanceParams,
    OrderScoringParams,
    PostOrdersArgs,
)

from config import Config

log = logging.getLogger("polyarb.client")

BUY = "BUY"
SELL = "SELL"


class AssetType:
    COLLATERAL = "COLLATERAL"
    CONDITIONAL = "CONDITIONAL"


POLYGON_RPC_URL = "https://polygon-rpc.com"
USDC_ADDRESS_POLYGON = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
ONCHAIN_BALANCE_CACHE_TTL_SECONDS = 3.0


class PolyClient:
    """Full-featured wrapper around the official py-clob-client."""

    def __init__(self, cfg: Config):
        self.cfg = cfg
        self._builder_config = None

        # Set up builder config if credentials provided
        if cfg.has_builder_config:
            try:
                from py_builder_signing_sdk.config import BuilderConfig, BuilderApiKeyCreds
                self._builder_config = BuilderConfig(
                    local_builder_creds=BuilderApiKeyCreds(
                        key=cfg.builder_api_key,
                        secret=cfg.builder_secret,
                        passphrase=cfg.builder_passphrase,
                    )
                )
                log.info("Builder config loaded -- orders will be attributed for fee reductions & rewards.")
            except Exception as e:
                log.warning("Failed to load builder config: %s -- continuing without builder.", e)

        self.client = ClobClient(
            host=cfg.clob_host,
            key=cfg.private_key,
            chain_id=cfg.chain_id,
            funder=cfg.funder_address,
            builder_config=self._builder_config,
        )
        self.close_only = False

        # Heartbeat state
        self._heartbeat_id: Optional[str] = None
        self._heartbeat_thread: Optional[threading.Thread] = None
        self._heartbeat_running = False

        # Orderbook hash cache for change detection
        self._ob_hash_cache: dict[str, str] = {}

        # Reused HTTP session + short TTL cache for on-chain balance checks.
        self._rpc_session = requests.Session()
        self._cache_lock = threading.Lock()
        self._onchain_usdc_cache_value = 0.0
        self._onchain_usdc_cache_ts = 0.0

    def authenticate(self) -> None:
        """Derive or create API credentials and attach them to the client."""
        log.info("Deriving API credentials...")
        creds = self.client.create_or_derive_api_creds()
        self.client.set_api_creds(creds)

        # Check if account is restricted
        try:
            result = self.client.get_closed_only_mode()
            # API may return a dict like {"closed_only": true} or a bool
            if isinstance(result, dict):
                self.close_only = bool(result.get("closed_only", False))
            else:
                self.close_only = bool(result)
            if self.close_only:
                log.warning("ACCOUNT IS IN CLOSE-ONLY MODE -- trading restricted!")
            else:
                log.info("Account status: normal (can place orders)")
        except Exception as e:
            log.debug("Could not check close-only status: %s", e)

        log.info("Authenticated successfully.")

    # ── Health & Status ──────────────────────────────────────────

    def is_server_up(self) -> bool:
        """Quick health check before trading."""
        try:
            self.client.get_ok()
            return True
        except Exception:
            return False

    def get_server_time(self) -> int:
        """Server timestamp for GTD expiry calculation."""
        return self.client.get_server_time()

    # ── Market Data — Single ─────────────────────────────────────

    def get_order_book(self, token_id: str):
        """Fetch the current order book for a token."""
        return self.client.get_order_book(token_id)

    @staticmethod
    def _iter_book_levels(order_book, side: str):
        """
        Read orderbook levels from either py-clob objects or WS/REST dict payloads.
        """
        if order_book is None:
            return []
        if isinstance(order_book, dict):
            levels = order_book.get(side)
            if levels is None and side == "asks":
                levels = order_book.get("sells")
            if levels is None and side == "bids":
                levels = order_book.get("buys")
            return levels or []
        return getattr(order_book, side, []) or []

    @staticmethod
    def _parse_level(level) -> tuple[float, float] | None:
        """Parse one price level into (price, size)."""
        try:
            if isinstance(level, dict):
                return float(level.get("price", 0)), float(level.get("size", 0))
            return float(level.price), float(level.size)
        except (AttributeError, TypeError, ValueError):
            return None

    def get_best_ask(self, order_book) -> tuple[float, float] | None:
        """Return (price, size) of the best ask, or None if empty."""
        asks = self._iter_book_levels(order_book, "asks")
        if not asks:
            return None

        best_price = float("inf")
        best_size = 0.0
        for level in asks:
            parsed = self._parse_level(level)
            if parsed is None:
                continue
            price, size = parsed
            if price < best_price:
                best_price, best_size = price, size

        if best_price == float("inf"):
            return None
        return best_price, best_size

    def get_best_bid(self, order_book) -> tuple[float, float] | None:
        """Return (price, size) of the best bid, or None if empty."""
        bids = self._iter_book_levels(order_book, "bids")
        if not bids:
            return None

        best_price = float("-inf")
        best_size = 0.0
        for level in bids:
            parsed = self._parse_level(level)
            if parsed is None:
                continue
            price, size = parsed
            if price > best_price:
                best_price, best_size = price, size

        if best_price == float("-inf"):
            return None
        return best_price, best_size

    def get_spread(self, token_id: str) -> dict | None:
        """Get bid-ask spread for a single token."""
        try:
            return self.client.get_spread(token_id)
        except Exception:
            return None

    def get_midpoint(self, token_id: str) -> float | None:
        """Get mid-market price (faster than parsing full orderbook)."""
        try:
            result = self.client.get_midpoint(token_id)
            return float(result.get("mid", 0))
        except Exception:
            return None

    # ── Market Data — Batch (massive efficiency gains) ───────────

    def get_order_books_batch(self, token_ids: list[str]) -> list:
        """
        Fetch orderbooks for up to 500 tokens in a SINGLE API call.
        This replaces N individual get_order_book() calls.
        """
        if not token_ids:
            return []

        results = []
        # Batch in chunks of 500 (API limit)
        for i in range(0, len(token_ids), 500):
            chunk = token_ids[i:i + 500]
            params = [BookParams(token_id=tid) for tid in chunk]
            try:
                batch_result = self.client.get_order_books(params)
                results.extend(batch_result)
            except Exception as e:
                log.error("Batch orderbook fetch failed: %s", e)
                # Fallback to individual fetches for this chunk
                for tid in chunk:
                    try:
                        results.append(self.client.get_order_book(tid))
                    except Exception:
                        results.append(None)
        return results

    def get_spreads_batch(self, token_ids: list[str]) -> list[dict]:
        """
        Fetch spreads for up to 500 tokens at once.
        Use for fast pre-filtering before fetching full orderbooks.
        """
        if not token_ids:
            return []

        results = []
        for i in range(0, len(token_ids), 500):
            chunk = token_ids[i:i + 500]
            params = [BookParams(token_id=tid) for tid in chunk]
            try:
                batch_result = self.client.get_spreads(params)
                results.extend(batch_result)
            except Exception as e:
                log.error("Batch spread fetch failed: %s", e)
                results.extend([None] * len(chunk))
        return results

    def get_midpoints_batch(self, token_ids: list[str]) -> list[dict]:
        """Fetch midpoints for up to 500 tokens at once."""
        if not token_ids:
            return []
        results = []
        for i in range(0, len(token_ids), 500):
            chunk = token_ids[i:i + 500]
            params = [BookParams(token_id=tid) for tid in chunk]
            try:
                batch_result = self.client.get_midpoints(params)
                results.extend(batch_result)
            except Exception as e:
                log.error("Batch midpoint fetch failed: %s", e)
                results.extend([None] * len(chunk))
        return results

    # ── Per-Market Fee Rate ──────────────────────────────────────

    def get_fee_rate_bps(self, token_id: str) -> int:
        """
        Get the fee rate in basis points for a specific market.
        Most prediction markets return 0 (no fees!).
        Only 15-min crypto markets have fees.
        Results are cached by the underlying client.
        """
        try:
            return self.client.get_fee_rate_bps(token_id)
        except Exception:
            return 0  # Default to 0 if lookup fails (safe assumption for most markets)

    def get_neg_risk(self, token_id: str) -> bool:
        """Check if a market uses the neg-risk exchange."""
        try:
            return self.client.get_neg_risk(token_id)
        except Exception:
            return False

    # ── Orderbook Hash Caching ───────────────────────────────────

    def has_orderbook_changed(self, token_id: str, order_book) -> bool:
        """
        Check if an orderbook has changed since we last saw it.
        Returns True if changed (or first time), False if identical.
        """
        try:
            current_hash = self.client.get_order_book_hash(order_book)
        except Exception:
            return True  # Assume changed if we can't hash

        old_hash = self._ob_hash_cache.get(token_id)
        self._ob_hash_cache[token_id] = current_hash

        if old_hash is None:
            return True
        return current_hash != old_hash

    # ── Balance & Allowance ──────────────────────────────────────

    def get_usdc_balance(self) -> float:
        """Get available USDC balance for trading (CLOB collateral)."""
        try:
            result = self.client.get_balance_allowance(
                BalanceAllowanceParams(asset_type=AssetType.COLLATERAL)
            )
            return float(result.get("balance", 0))
        except Exception as e:
            log.error("Failed to get USDC balance: %s", e)
            return 0.0

    def get_onchain_usdc_balance(self, use_cache: bool = True) -> float:
        """Get USDC balance in the wallet on Polygon (not yet deposited to CLOB)."""
        now = time.time()
        if use_cache:
            with self._cache_lock:
                if (now - self._onchain_usdc_cache_ts) < ONCHAIN_BALANCE_CACHE_TTL_SECONDS:
                    return self._onchain_usdc_cache_value

        wallet = self.cfg.funder_address
        data = "0x70a08231" + wallet[2:].lower().zfill(64)
        payload = {
            "jsonrpc": "2.0", "id": 1, "method": "eth_call",
            "params": [{"to": USDC_ADDRESS_POLYGON, "data": data}, "latest"]
        }
        try:
            resp = self._rpc_session.post(POLYGON_RPC_URL, json=payload, timeout=10)
            resp.raise_for_status()
            hex_balance = resp.json().get("result", "0x0")
            balance = int(hex_balance, 16) / 1e6  # USDC has 6 decimals
            with self._cache_lock:
                self._onchain_usdc_cache_value = balance
                self._onchain_usdc_cache_ts = now
            return balance
        except (requests.RequestException, ValueError, TypeError) as e:
            log.error("Failed to get on-chain USDC balance: %s", e)
            return 0.0

    def get_token_balance(self, token_id: str) -> float:
        """Get balance of a specific conditional token."""
        try:
            result = self.client.get_balance_allowance(
                BalanceAllowanceParams(asset_type=AssetType.CONDITIONAL, token_id=token_id)
            )
            return float(result.get("balance", 0))
        except Exception as e:
            log.error("Failed to get token balance: %s", e)
            return 0.0

    # ── Order Placement — Single ─────────────────────────────────

    def place_limit_buy(self, token_id: str, price: float, size: float,
                        order_type: OrderType = OrderType.GTC,
                        expiration: int = 0) -> dict:
        """Place a limit buy order (GTC or GTD)."""
        order_args = OrderArgs(
            token_id=token_id,
            price=price,
            size=size,
            side=BUY,
            expiration=expiration,
        )
        signed = self.client.create_order(order_args)
        response = self.client.post_order(signed, orderType=order_type)
        log.info("BUY order placed: token=%s price=%.4f size=%.2f type=%s resp=%s",
                 token_id[:12], price, size, order_type, response)
        return response

    def place_market_buy(self, token_id: str, price: float, size: float) -> dict:
        """Place a limit buy order at the given price (legacy compatibility)."""
        return self.place_limit_buy(token_id, price, size)

    def place_fok_buy(self, token_id: str, amount: float) -> dict:
        """
        Place a Fill-Or-Kill buy order.
        Amount = USDC to spend. Price is auto-calculated from current orderbook.
        Fills entirely or not at all — no partial fill risk.
        """
        order_args = MarketOrderArgs(
            token_id=token_id,
            amount=amount,
            side=BUY,
            order_type=OrderType.FOK,
        )
        signed = self.client.create_market_order(order_args)
        response = self.client.post_order(signed, orderType=OrderType.FOK)
        log.info("FOK BUY: token=%s amount=$%.2f resp=%s", token_id[:12], amount, response)
        return response

    def place_market_sell(self, token_id: str, price: float, size: float) -> dict:
        """Place a limit sell order at the given price."""
        order_args = OrderArgs(
            token_id=token_id,
            price=price,
            size=size,
            side=SELL,
        )
        signed = self.client.create_order(order_args)
        response = self.client.post_order(signed)
        log.info("SELL order placed: token=%s price=%.4f size=%.2f resp=%s",
                 token_id[:12], price, size, response)
        return response

    # ── Order Placement — Batch (critical for multi-leg arbs) ────

    def place_batch_orders(self, orders: list[dict]) -> dict:
        """
        Submit multiple orders in a SINGLE API call.
        Reduces race condition risk dramatically for multi-leg arbs.

        Each order dict: {token_id, price, size, side, order_type, expiration}
        """
        args_list = []
        for o in orders:
            order_type = o.get("order_type", OrderType.GTC)
            expiration = o.get("expiration", 0)

            order_args = OrderArgs(
                token_id=o["token_id"],
                price=o["price"],
                size=o["size"],
                side=o.get("side", BUY),
                expiration=expiration,
            )
            signed = self.client.create_order(order_args)
            args_list.append(PostOrdersArgs(
                order=signed,
                orderType=order_type,
            ))

        response = self.client.post_orders(args_list)
        if isinstance(response, list):
            if any(isinstance(r, dict) and r.get("errorMsg") == "invalid signature" for r in response):
                log.error(
                    "Order signature invalid. Check PRIVATE_KEY and FUNDER_ADDRESS are from the same Polymarket account."
                )
        log.info("BATCH order placed: %d legs -> %s", len(orders), response)
        return response

    def place_batch_fok_orders(self, orders: list[dict]) -> dict:
        """
        Submit multiple FOK orders.
        Each order dict: {token_id, amount}  (amount in USDC)
        """
        args_list = []
        for o in orders:
            order_args = MarketOrderArgs(
                token_id=o["token_id"],
                amount=o["amount"],
                side=BUY,
                order_type=OrderType.FOK,
            )
            signed = self.client.create_market_order(order_args)
            args_list.append(PostOrdersArgs(
                order=signed,
                orderType=OrderType.FOK,
            ))

        response = self.client.post_orders(args_list)
        log.info("BATCH FOK order placed: %d legs -> %s", len(orders), response)
        return response

    # ── Order Management ─────────────────────────────────────────

    def get_open_orders(self) -> list:
        """Get all open orders for the authenticated user."""
        return self.client.get_orders()

    def cancel_order(self, order_id: str) -> dict:
        """Cancel a specific order."""
        return self.client.cancel(order_id)

    def cancel_orders(self, order_ids: list[str]) -> dict:
        """Cancel multiple orders at once."""
        return self.client.cancel_orders(order_ids)

    def cancel_all_orders(self) -> dict:
        """Cancel all open orders."""
        return self.client.cancel_all()

    def cancel_market_orders(self, market: str = "", asset_id: str = "") -> dict:
        """Cancel all orders for a specific market."""
        return self.client.cancel_market_orders(market=market, asset_id=asset_id)

    # ── Trade History ────────────────────────────────────────────

    def get_trades(self, market: str = None) -> list:
        """Get trade history, optionally filtered by market."""
        from py_clob_client.clob_types import TradeParams
        params = TradeParams(market=market) if market else None
        return self.client.get_trades(params)

    def get_order(self, order_id: str) -> dict:
        """Get details of a specific order."""
        return self.client.get_order(order_id)

    # ── Heartbeat Dead Man's Switch ──────────────────────────────

    def start_heartbeat(self, interval: int = 5) -> None:
        """
        Start sending heartbeats every `interval` seconds.
        If a heartbeat isn't sent within 10 seconds, ALL open orders are auto-cancelled.
        Critical safety mechanism — if the bot crashes, orders don't sit dangerously.
        """
        if self._heartbeat_running:
            return

        self._heartbeat_running = True
        self._heartbeat_thread = threading.Thread(
            target=self._heartbeat_loop,
            args=(interval,),
            daemon=True,
        )
        self._heartbeat_thread.start()
        log.info("Heartbeat started (interval=%ds). Orders auto-cancel if bot dies.", interval)

    def _heartbeat_loop(self, interval: int) -> None:
        """Background thread that sends heartbeats."""
        while self._heartbeat_running:
            try:
                resp = self.client.post_heartbeat(self._heartbeat_id)
                if isinstance(resp, dict):
                    self._heartbeat_id = resp.get("heartbeat_id", self._heartbeat_id)
                log.debug("Heartbeat sent: %s", self._heartbeat_id)
            except Exception as e:
                log.error("Heartbeat FAILED: %s -- resetting ID for fresh start", e)
                self._heartbeat_id = None  # Reset so next attempt creates a new heartbeat
            time.sleep(interval)

    def stop_heartbeat(self) -> None:
        """Stop the heartbeat background thread."""
        if not self._heartbeat_running:
            return
        self._heartbeat_running = False
        if self._heartbeat_thread and self._heartbeat_thread.is_alive():
            self._heartbeat_thread.join(timeout=10)
        log.info("Heartbeat stopped.")

    # ── Reward Scoring ───────────────────────────────────────────

    def is_order_scoring(self, order_id: str) -> bool:
        """Check if an order is earning liquidity rewards."""
        try:
            result = self.client.is_order_scoring(OrderScoringParams(orderId=order_id))
            return bool(result.get("scoring", False))
        except Exception:
            return False
