"""
Polymarket Arbitrage Bot — Main entry point.

Supports two modes:
  1. WebSocket mode (default): Real-time orderbook updates, ~100ms latency
  2. Polling mode (fallback): Fetch → Scan → Execute → Sleep cycle

Features:
  - Batch orderbook fetching (2 API calls instead of 1000)
  - Per-market fee rates (most markets = 0% fees!)
  - Batch order placement (all legs in 1 call)
  - FOK (Fill-Or-Kill) orders for guaranteed fills
  - GTD orders that auto-expire if not filled
  - Heartbeat dead man's switch (auto-cancel on crash)
  - Builder program integration for fee reductions
  - WebSocket with new_market + market_resolved events
  - CTF merge for profit realization
  - Balance pre-checks before trading
  - Position tracking and P&L reporting
"""

import signal
import sys
import time
import logging
import threading

from config import load_config
from logger import setup_logger
from client import PolyClient
from markets import fetch_active_markets
from arbitrage import scan_all_markets
from executor import Executor
from risk import RiskManager

shutdown_requested = False


def handle_signal(signum, frame):
    global shutdown_requested
    log = logging.getLogger("polyarb")
    log.info("Shutdown signal received. Finishing current cycle...")
    shutdown_requested = True


def run_websocket_mode(cfg, log, poly, risk, executor):
    """
    WebSocket mode: Real-time orderbook monitoring.
    Gets pushed updates instead of polling — sees arbs in ~100ms vs ~15s.
    """
    global shutdown_requested
    from websocket_client import PolyWebSocket

    # State shared between WS callbacks and the arb scanner
    live_books: dict[str, dict] = {}      # token_id → latest orderbook data
    book_lock = threading.Lock()
    markets_by_token: dict[str, object] = {}  # token_id → Market
    all_markets: list = []

    def on_book_update(data):
        """Called when a full orderbook snapshot is pushed."""
        asset_id = data.get("asset_id", "")
        if not asset_id:
            return
        with book_lock:
            live_books[asset_id] = data

    def on_price_change(data):
        """Called on order placement/cancellation — indicates book changed."""
        # price_change tells us the book moved, but we use the
        # full book snapshots for arb detection
        pass

    def on_best_bid_ask(data):
        """BBO update — fast signal that spread changed."""
        asset_id = data.get("asset_id", "")
        best_ask = float(data.get("best_ask", 0) or 0)
        best_bid = float(data.get("best_bid", 0) or 0)
        spread = float(data.get("spread", 1) or 1)

        # Quick check: can this asset be part of an arb?
        # If best_ask is very low, the complementary outcome might complete an arb
        if best_ask > 0 and best_ask < 0.55:
            log.debug("Low ask signal: %s @ %.4f (spread=%.4f)", asset_id[:12], best_ask, spread)

    def on_new_market(data):
        """New market created — first-mover advantage on mispriced markets."""
        question = data.get("question", "")
        assets = data.get("assets_ids", [])
        log.info("NEW MARKET: '%s' with %d outcomes", question[:60], len(assets))

        # Subscribe to the new market's assets for monitoring
        if assets:
            ws_client.subscribe(assets)

    def on_market_resolved(data):
        """Market resolved — trigger position settlement."""
        question = data.get("question", "")
        condition_id = data.get("market", "")
        winning = data.get("winning_outcome", "")
        log.info("MARKET RESOLVED: '%s' → %s", question[:60], winning)

        # Free up the exposure for this market
        if condition_id:
            risk.settle_all_for_market(condition_id)

    # Initialize WebSocket
    ws_client = PolyWebSocket(
        ws_url=cfg.ws_host,
        on_book_update=on_book_update,
        on_price_change=on_price_change,
        on_best_bid_ask=on_best_bid_ask,
        on_new_market=on_new_market,
        on_market_resolved=on_market_resolved,
    )

    # Initial market discovery (still needed to know which tokens to subscribe to)
    log.info("Fetching initial markets...")
    all_markets = fetch_active_markets(limit=500, min_liquidity=cfg.min_market_liquidity)
    log.info("Found %d candidate markets", len(all_markets))

    # Collect all token IDs and subscribe
    all_token_ids = []
    for market in all_markets:
        for outcome in market.outcomes:
            all_token_ids.append(outcome.token_id)
            markets_by_token[outcome.token_id] = market

    ws_client.connect(all_token_ids)
    log.info("WebSocket subscribed to %d assets. Waiting for data...", len(all_token_ids))

    # Give WebSocket time to receive initial book snapshots
    time.sleep(3)

    # Arb scanning loop — runs on WS-pushed data
    cycle = 0
    total_arbs_found = 0
    total_arbs_executed = 0

    while not shutdown_requested:
        cycle += 1

        try:
            # Use the batch REST endpoint for a full snapshot periodically
            # The WS updates are incremental; we do a full refresh every N cycles
            if cycle == 1 or cycle % 20 == 0:
                log.info("--- Full market refresh (cycle %d) ---", cycle)
                all_markets = fetch_active_markets(limit=500, min_liquidity=cfg.min_market_liquidity)

                # Discover new tokens to subscribe to
                new_tokens = []
                for market in all_markets:
                    for outcome in market.outcomes:
                        if outcome.token_id not in markets_by_token:
                            new_tokens.append(outcome.token_id)
                        markets_by_token[outcome.token_id] = market

                if new_tokens:
                    ws_client.subscribe(new_tokens)
                    log.info("Subscribed to %d new tokens", len(new_tokens))

            # Scan using batch orderbook fetch (fast even without WS data)
            opps = scan_all_markets(
                poly=poly,
                markets=all_markets,
                min_profit=cfg.min_profit_margin,
                min_depth=cfg.min_book_depth,
                min_arb_value=cfg.min_arb_value,
                min_cost_threshold=cfg.min_cost_threshold,
                max_profit_per_share=cfg.max_profit_per_share,
            )

            total_arbs_found += len(opps)

            if opps:
                log.info("Found %d arbitrage opportunities:", len(opps))
                for i, opp in enumerate(opps, 1):
                    fee_label = f"fee={opp.fee_rate_bps}bps" if opp.fee_rate_bps > 0 else "FREE"
                    log.info(
                        "  #%d: '%s' | profit=$%.4f/sh | max=%d | est=$%.2f | %s",
                        i, opp.market.question[:50], opp.profit_per_share,
                        int(opp.max_shares), opp.estimated_profit, fee_label,
                    )

                # Execute best opportunities
                if risk.can_trade():
                    for opp in opps:
                        if not risk.can_trade() or shutdown_requested:
                            break
                        success = executor.execute_arb(opp)
                        if success:
                            total_arbs_executed += 1
                else:
                    log.warning("Risk limits reached. %s", risk.summary())

            # Brief sleep — WS mode doesn't need long intervals
            if not shutdown_requested:
                time.sleep(2)  # 2s between scans vs 15s in polling mode

        except KeyboardInterrupt:
            break
        except Exception as e:
            log.error("Error in WS cycle %d: %s", cycle, e, exc_info=True)
            time.sleep(5)

    # Cleanup
    ws_client.disconnect()
    return cycle, total_arbs_found, total_arbs_executed


def run_polling_mode(cfg, log, poly, risk, executor):
    """
    Polling mode: Fetch → Scan → Execute → Sleep.
    Fallback when WebSocket is disabled.
    Still uses batch orderbook fetching for efficiency.
    """
    global shutdown_requested

    cycle = 0
    total_arbs_found = 0
    total_arbs_executed = 0

    while not shutdown_requested:
        cycle += 1
        log.info("--- Cycle %d ---", cycle)

        try:
            # 1. Fetch markets (pre-filtered by Gamma prices)
            markets = fetch_active_markets(limit=500, min_liquidity=cfg.min_market_liquidity)
            log.info("Scanning %d candidate markets...", len(markets))

            if not markets:
                log.warning("No active markets found. Retrying next cycle.")
                time.sleep(cfg.scan_interval)
                continue

            # 2. Scan for arbitrage (uses batch orderbook fetch internally)
            opps = scan_all_markets(
                poly=poly,
                markets=markets,
                min_profit=cfg.min_profit_margin,
                min_depth=cfg.min_book_depth,
                min_arb_value=cfg.min_arb_value,
                min_cost_threshold=cfg.min_cost_threshold,
                max_profit_per_share=cfg.max_profit_per_share,
            )

            total_arbs_found += len(opps)

            if not opps:
                log.info("No arbitrage opportunities found.")
            else:
                log.info("Found %d arbitrage opportunities:", len(opps))
                for i, opp in enumerate(opps, 1):
                    fee_label = f"fee={opp.fee_rate_bps}bps" if opp.fee_rate_bps > 0 else "FREE"
                    log.info(
                        "  #%d: '%s' | profit=$%.4f/sh | max=%d | est=$%.2f | %s",
                        i, opp.market.question[:50], opp.profit_per_share,
                        int(opp.max_shares), opp.estimated_profit, fee_label,
                    )

                # 3. Execute (best opportunity first)
                if risk.can_trade():
                    for opp in opps:
                        if not risk.can_trade() or shutdown_requested:
                            break
                        success = executor.execute_arb(opp)
                        if success:
                            total_arbs_executed += 1
                else:
                    log.warning("Risk limits reached — no more trades allowed. %s", risk.summary())

            # 4. Status summary
            log.info("Cycle %d complete. %s | This cycle: %d arbs | Lifetime: %d/%d",
                     cycle, risk.summary(), len(opps),
                     total_arbs_found, total_arbs_executed)

        except KeyboardInterrupt:
            break
        except Exception as e:
            log.error("Error in cycle %d: %s", cycle, e, exc_info=True)

        # 5. Sleep
        if not shutdown_requested:
            log.info("Sleeping %ds...", cfg.scan_interval)
            time.sleep(cfg.scan_interval)

    return cycle, total_arbs_found, total_arbs_executed


def main():
    global shutdown_requested

    # Load config and set up logging
    cfg = load_config()
    log = setup_logger(cfg.log_level)

    log.info("=" * 60)
    log.info("  Polymarket Arbitrage Bot v2.0")
    log.info("=" * 60)
    log.info("Mode: %s", "DRY RUN (no real trades)" if cfg.dry_run else "LIVE TRADING")
    log.info("Min profit margin: $%.4f per share", cfg.min_profit_margin)
    log.info("Max position size: $%.2f", cfg.max_position_size)
    log.info("Max total exposure: $%.2f", cfg.max_total_exposure)
    log.info("Fees: Per-market lookup (most = 0%%)")
    log.info("Data mode: %s", "WebSocket (real-time)" if cfg.ws_enabled else "Polling")
    log.info("Execution: %s",
             f"batch={'ON' if cfg.use_batch_orders else 'OFF'} "
             f"| FOK={'ON' if cfg.use_fok_orders else 'OFF'} "
             f"| GTD={cfg.gtd_expiry_seconds}s")
    log.info("Builder: %s", "ENABLED" if cfg.has_builder_config else "disabled")
    log.info("Heartbeat: %s", f"ON ({cfg.heartbeat_interval}s)" if cfg.heartbeat_enabled else "OFF")
    log.info("Balance check: %s", "ON" if cfg.balance_check_enabled else "OFF")
    log.info("Sanity filters: min_cost=$%.2f | max_profit/share=$%.2f | min_arb=$%.2f | min_liq=$%.0f",
             cfg.min_cost_threshold, cfg.max_profit_per_share, cfg.min_arb_value, cfg.min_market_liquidity)
    log.info("=" * 60)

    # Initialize components
    poly = PolyClient(cfg)
    poly.authenticate()

    # Server health check
    if not poly.is_server_up():
        log.error("CLOB server is not responding! Aborting.")
        sys.exit(1)
    log.info("CLOB server: OK")

    # Close-only mode check — account is restricted from placing new orders
    if poly.close_only:
        if not cfg.dry_run:
            log.error("Account is in CLOSE-ONLY MODE — cannot place orders! Aborting.")
            log.error("Check your account status at https://polymarket.com")
            sys.exit(1)
        else:
            log.warning("Account is in CLOSE-ONLY MODE — scanning only (dry run).")

    # Pre-flight balance check
    if cfg.balance_check_enabled:
        clob_balance = poly.get_usdc_balance()
        wallet_balance = poly.get_onchain_usdc_balance()
        total_available = max(clob_balance, wallet_balance)
        log.info("USDC balance: $%.2f (CLOB: $%.2f | Wallet: $%.2f)",
                 total_available, clob_balance, wallet_balance)
        if total_available < 1.0 and not cfg.dry_run:
            log.error("Insufficient USDC for live trading!")
            sys.exit(1)

    risk = RiskManager(cfg)
    executor = Executor(poly, risk, cfg, dry_run=cfg.dry_run)

    # Start heartbeat (dead man's switch) — auto-cancels all orders if bot crashes
    if cfg.heartbeat_enabled and not cfg.dry_run:
        poly.start_heartbeat(interval=cfg.heartbeat_interval)

    # Graceful shutdown on Ctrl+C
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    # Run the main trading loop
    try:
        if cfg.ws_enabled:
            cycle, total_found, total_exec = run_websocket_mode(cfg, log, poly, risk, executor)
        else:
            cycle, total_found, total_exec = run_polling_mode(cfg, log, poly, risk, executor)
    except Exception as e:
        log.error("Fatal error: %s", e, exc_info=True)
        cycle, total_found, total_exec = 0, 0, 0

    # Shutdown
    if cfg.heartbeat_enabled:
        poly.stop_heartbeat()

    log.info("=" * 60)
    log.info("Bot shutting down.")
    log.info("Total cycles: %d | Arbs found: %d | Arbs executed: %d", cycle, total_found, total_exec)
    log.info("P&L Summary: %s", risk.summary())

    if executor.trade_log:
        log.info("Trade log:")
        for t in executor.trade_log:
            status = "DRY" if t["dry_run"] else ("FAIL" if t["failed"] else "OK")
            fee_label = f"fee={t.get('fee_rate_bps', '?')}bps" if t.get("fee_rate_bps", 0) > 0 else "FREE"
            log.info("  [%s] %s | %d shares | cost=$%.2f | profit=$%.4f | %s",
                     status, t["market"][:40], t["shares"], t["cost"], t["expected_profit"], fee_label)
    log.info("=" * 60)


if __name__ == "__main__":
    main()
