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

from py_clob_client.clob_types import OrderType

from arbitrage import ArbOpportunity
from client import PolyClient
from risk import RiskManager
from config import Config

log = logging.getLogger("polyarb.executor")


class Executor:
    """Handles safe execution of arbitrage trades with batch orders."""

    def __init__(self, poly: PolyClient, risk: "RiskManager", cfg: Config, dry_run: bool = True):
        self.poly = poly
        self.risk = risk
        self.cfg = cfg
        self.dry_run = dry_run
        self.trade_log: list[dict] = []

    def execute_arb(self, opp: ArbOpportunity) -> bool:
        """
        Execute an arbitrage opportunity by buying all legs.
        Returns True if all legs were filled, False otherwise.
        """
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

        total_cost = shares * cost_per_set
        fee_label = f"fee={opp.fee_rate_bps}bps" if opp.fee_rate_bps > 0 else "NO FEES"
        log.info(
            "Executing arb: '%s' | %d shares | cost=$%.2f | profit=$%.4f | %s",
            opp.market.question[:50], shares, total_cost, opp.profit_per_share * shares, fee_label,
        )

        if self.dry_run:
            log.info("DRY RUN -- trade NOT submitted.")
            self._record_trade(opp, shares, total_cost, dry_run=True)
            self.risk.record_exposure(total_cost)
            return True

        # 2. Pre-trade balance check
        if self.cfg.balance_check_enabled:
            clob_balance = self.poly.get_usdc_balance()
            wallet_balance = self.poly.get_onchain_usdc_balance()
            available = max(clob_balance, wallet_balance)
            if available < total_cost:
                log.warning(
                    "Insufficient USDC balance: available=$%.2f (CLOB=$%.2f, wallet=$%.2f) < needed=$%.2f",
                    available,
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
            self.risk.record_exposure(total_cost)
            self._record_trade(opp, shares, total_cost)
            log.info("ARB EXECUTED SUCCESSFULLY: '%s'", opp.market.question[:50])
        else:
            self._record_trade(opp, shares, total_cost, failed=True)

        return success

    def _execute_batch(self, opp: ArbOpportunity, shares: int) -> bool:
        """
        Submit ALL arb legs in a SINGLE API call.
        Dramatically reduces race condition risk vs sequential execution.
        """
        # Build order list for batch submission
        orders = []
        order_type = OrderType.GTC
        expiration = 0

        # Use GTD with short expiry if configured
        # API requires: expiration >= now + 60s (security threshold) + desired_expiry
        if self.cfg.gtd_expiry_seconds > 0:
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

            # Check response for actual success — API may return 'success':True but with errorMsg
            if isinstance(resp, list):
                for leg in resp:
                    if isinstance(leg, dict):
                        err = leg.get("errorMsg", "")
                        order_id = leg.get("orderID", "")
                        if err or not order_id:
                            log.error("Batch leg REJECTED: %s", err or "no orderID returned")
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
                    # FOK: Fill entire leg or reject — no partial fill risk
                    amount = shares * ask_price
                    resp = self.poly.place_fok_buy(token_id=token_id, amount=amount)
                else:
                    resp = self.poly.place_limit_buy(
                        token_id=token_id,
                        price=ask_price,
                        size=shares,
                    )
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
            "fee_rate_bps": opp.fee_rate_bps,
            "dry_run": dry_run,
            "failed": failed,
            "error": error,
            "timestamp": time.time(),
        })
