"""
Order execution — takes an ArbOpportunity and buys all outcome legs.

Upgrades:
  - Batch order placement (all legs in 1 API call) to minimize race conditions
  - FOK (Fill-Or-Kill) orders for guaranteed all-or-nothing fills
  - GTD (Good-Til-Date) orders that auto-expire if not filled quickly
  - Pre-trade USDC balance validation
  - Per-market fee awareness (most markets = 0% fees)
"""

import logging
import time
from typing import TYPE_CHECKING

try:
    from py_clob_client.clob_types import OrderType
except Exception:  # pragma: no cover - allows lightweight local unit tests without full SDK deps
    class OrderType:
        GTC = "GTC"
        FOK = "FOK"
        GTD = "GTD"

from arbitrage import ArbOpportunity
from risk import RiskManager
from config import Config

if TYPE_CHECKING:
    from client import PolyClient

log = logging.getLogger("polyarb.executor")


class Executor:
    """Handles safe execution of arbitrage trades with batch orders."""

    def __init__(self, poly: "PolyClient", risk: "RiskManager", cfg: Config, dry_run: bool = True):
        self.poly = poly
        self.risk = risk
        self.cfg = cfg
        self.dry_run = dry_run
        self.trade_log: list[dict] = []
        self._market_cooldowns: dict[str, float] = {}

    @staticmethod
    def _normalize_condition_id(condition_id: str) -> str:
        cid = (condition_id or "").strip().lower()
        return cid[2:] if cid.startswith("0x") else cid

    def _cooldown_remaining(self, condition_id: str) -> float:
        if self.cfg.failure_cooldown_seconds <= 0:
            return 0.0
        cid = self._normalize_condition_id(condition_id)
        if not cid:
            return 0.0
        now = time.time()
        expires_at = self._market_cooldowns.get(cid, 0.0)
        if expires_at <= now:
            self._market_cooldowns.pop(cid, None)
            return 0.0
        return expires_at - now

    def _set_failure_cooldown(self, condition_id: str) -> None:
        if self.cfg.failure_cooldown_seconds <= 0:
            return
        cid = self._normalize_condition_id(condition_id)
        if not cid:
            return
        expires_at = time.time() + self.cfg.failure_cooldown_seconds
        self._market_cooldowns[cid] = expires_at
        log.info(
            "Market cooldown enabled for %s (%.0fs after failed attempt).",
            cid[:20],
            self.cfg.failure_cooldown_seconds,
        )

    @staticmethod
    def _status_is_matched(status: str) -> bool:
        return str(status or "").strip().lower() == "matched"

    def _validate_order_response(self, response: dict, context: str) -> bool:
        """Validate a placement response means the leg is truly executed."""
        if not isinstance(response, dict):
            log.error("%s: malformed response: %r", context, response)
            return False

        success = response.get("success", True)
        error = str(response.get("errorMsg", "") or "")
        order_id = response.get("orderID") or response.get("orderId") or ""
        status = str(response.get("status", "") or "")

        if success is False:
            log.error("%s: server-side failure: %s", context, error or "unknown")
            return False
        if error:
            log.error("%s: placement error: %s", context, error)
            return False
        if not order_id:
            log.error("%s: missing order ID in response", context)
            return False

        if self.cfg.require_full_match and not self._status_is_matched(status):
            log.error(
                "%s: order accepted but not immediately matched (status=%s) -- aborting arb.",
                context,
                status or "unknown",
            )
            return False

        return True

    def execute_arb(self, opp: ArbOpportunity) -> bool:
        """
        Execute an arbitrage opportunity by buying all legs.
        Returns True if all legs were filled, False otherwise.
        """
        cooldown_remaining = self._cooldown_remaining(opp.market.condition_id)
        if cooldown_remaining > 0:
            log.debug(
                "Skipping '%s': market is on %.1fs cooldown after recent failure.",
                opp.market.question[:50],
                cooldown_remaining,
            )
            return False

        # 1. Determine position size (capped by risk limits)
        desired_shares = opp.max_shares
        allowed_cost = self.risk.max_allowed_cost()
        cost_per_set = opp.total_cost_with_fees
        max_affordable = allowed_cost / cost_per_set if cost_per_set > 0 else 0
        shares = min(desired_shares, max_affordable)

        if shares < 1:
            log.warning("Cannot execute arb: risk limits prevent trade (allowed=$%.2f, need=$%.4f/share)",
                        allowed_cost, cost_per_set)
            return False

        shares = int(shares)  # Polymarket uses whole shares
        if shares < 1:
            log.warning("Cannot execute arb: rounded share size is < 1.")
            return False

        total_cost = shares * cost_per_set
        fee_label = f"fee={opp.fee_rate_bps}bps" if opp.fee_rate_bps > 0 else "NO FEES"
        log.info(
            "Executing arb: '%s' | %d shares | cost=$%.2f | profit=$%.4f | %s",
            opp.market.question[:50], shares, total_cost, opp.profit_per_share * shares, fee_label,
        )

        if self.dry_run:
            log.info("DRY RUN -- trade NOT submitted.")
            self._record_trade(opp, shares, total_cost, dry_run=True)
            self.risk.record_exposure(
                total_cost,
                condition_id=opp.market.condition_id,
                question=opp.market.question,
            )
            return True

        # 2. Pre-trade balance check
        if self.cfg.balance_check_enabled:
            clob_balance = self.poly.get_usdc_balance()
            wallet_balance = self.poly.get_onchain_usdc_balance()
            if clob_balance < total_cost:
                log.warning(
                    "Insufficient CLOB collateral: CLOB=$%.2f, wallet=$%.2f, needed=$%.2f "
                    "(wallet funds are not immediately tradable until deposited)",
                    clob_balance,
                    wallet_balance,
                    total_cost,
                )
                return False

        # 3. Execute — choose strategy based on config
        if self.cfg.use_batch_orders:
            success = self._execute_batch(opp, shares)
        else:
            success = self._execute_sequential(opp, shares)

        if success:
            self._market_cooldowns.pop(self._normalize_condition_id(opp.market.condition_id), None)
            self.risk.record_exposure(
                total_cost,
                condition_id=opp.market.condition_id,
                question=opp.market.question,
            )
            self._record_trade(opp, shares, total_cost)
            log.info("ARB EXECUTED SUCCESSFULLY: '%s'", opp.market.question[:50])
        else:
            self.risk.record_failure()
            self._set_failure_cooldown(opp.market.condition_id)
            self._record_trade(opp, shares, total_cost, failed=True)

        return success

    def _execute_batch(self, opp: ArbOpportunity, shares: int) -> bool:
        """
        Submit ALL arb legs in a SINGLE API call.
        Dramatically reduces race condition risk vs sequential execution.
        """
        # Build order list for batch submission
        orders = []
        order_type = OrderType.FOK if self.cfg.use_fok_orders else OrderType.GTC
        expiration = 0

        # Use GTD with short expiry only when not using FOK.
        # API requires: expiration >= now + 60s (security threshold) + desired_expiry
        if not self.cfg.use_fok_orders and self.cfg.gtd_expiry_seconds > 0:
            order_type = OrderType.GTD
            security_threshold = 60  # Polymarket requires at least 1 minute buffer
            try:
                server_time = self.poly.get_server_time()
                if isinstance(server_time, dict):
                    now_ts = int(server_time.get("timestamp", time.time()))
                else:
                    now_ts = int(server_time)
            except (TypeError, ValueError):
                now_ts = int(time.time())
            expiration = now_ts + security_threshold + self.cfg.gtd_expiry_seconds

        for token_id, _, ask_price, _ in opp.legs:
            orders.append({
                "token_id": token_id,
                "price": ask_price,
                "size": shares,
                "side": "BUY",
                "order_type": order_type,
                "expiration": expiration,
            })

        try:
            resp = self.poly.place_batch_orders(orders)
            log.info("Batch arb response: %s", resp)

            if not isinstance(resp, list):
                log.error("Batch arb response malformed (expected list): %r", resp)
                self._emergency_cancel()
                return False
            if len(resp) != len(orders):
                log.error("Batch arb response length mismatch: expected=%d got=%d", len(orders), len(resp))
                self._emergency_cancel()
                return False

            for idx, leg in enumerate(resp, 1):
                if not self._validate_order_response(leg, context=f"Batch leg {idx}/{len(resp)}"):
                    self._emergency_cancel()
                    return False
            return True
        except Exception as e:
            log.error("BATCH ARB FAILED: %s -- attempting emergency cancel.", e)
            self._emergency_cancel()
            return False

    def _execute_sequential(self, opp: ArbOpportunity, shares: int) -> bool:
        """Fallback: execute each leg sequentially (higher risk of partial fills)."""
        for token_id, outcome_name, ask_price, _ in opp.legs:
            try:
                if self.cfg.use_fok_orders:
                    # FOK at explicit limit price keeps the arb bound deterministic.
                    resp = self.poly.place_limit_buy(
                        token_id=token_id,
                        price=ask_price,
                        size=shares,
                        order_type=OrderType.FOK,
                        expiration=0,
                    )
                else:
                    resp = self.poly.place_limit_buy(
                        token_id=token_id,
                        price=ask_price,
                        size=shares,
                    )
                if not self._validate_order_response(resp, context=f"Sequential leg {outcome_name}"):
                    self._emergency_cancel()
                    return False
                log.info("Leg filled: %s @ %.4f x %d → %s",
                         outcome_name, ask_price, shares, resp)
            except Exception as e:
                log.error("FAILED to fill leg %s: %s -- attempting emergency cancel.", outcome_name, e)
                self._emergency_cancel()
                return False
        return True

    def _emergency_cancel(self) -> None:
        """Cancel all open orders as a safety measure."""
        try:
            self.poly.cancel_all_orders()
            log.warning("Emergency cancel: all open orders cancelled.")
        except Exception as e:
            log.error("Emergency cancel FAILED: %s", e)

    def _record_trade(self, opp: ArbOpportunity, shares: int, cost: float,
                      dry_run: bool = False, failed: bool = False, error: str = "") -> None:
        self.trade_log.append({
            "market": opp.market.question,
            "condition_id": opp.market.condition_id,
            "shares": shares,
            "cost": cost,
            "profit_per_share": opp.profit_per_share,
            "expected_profit": opp.profit_per_share * shares,
            "roi": opp.roi,
            "fill_confidence": opp.fill_confidence,
            "priority_score": opp.priority_score,
            "fee_rate_bps": opp.fee_rate_bps,
            "dry_run": dry_run,
            "failed": failed,
            "error": error,
            "timestamp": time.time(),
        })
