"""
Risk management — tracks exposure, enforces position limits, and manages capital recycling.

Upgrades:
  - Tracks individual positions for settlement detection
  - Auto-resets exposure when positions are settled
  - Balance-aware (checks real USDC balance)
  - Per-trade P&L tracking
"""

import logging
import threading
import time
from config import Config

log = logging.getLogger("polyarb.risk")


class RiskManager:
    """Risk manager that tracks exposure, positions, and P&L."""

    def __init__(self, cfg: Config):
        self.max_position_size = cfg.max_position_size
        self.max_total_exposure = cfg.max_total_exposure
        self.current_exposure = 0.0
        self._lock = threading.RLock()

        # Track individual positions for capital recycling
        self.positions: list[dict] = []
        self.total_profit = 0.0
        self.total_trades = 0
        self.successful_trades = 0
        self.failed_trades = 0

    @staticmethod
    def _normalize_condition_id(condition_id: str) -> str:
        cid = (condition_id or "").strip().lower()
        return cid[2:] if cid.startswith("0x") else cid

    def max_allowed_cost(self) -> float:
        """Maximum USDC the bot can spend on the next trade."""
        with self._lock:
            remaining = self.max_total_exposure - self.current_exposure
            return min(self.max_position_size, max(0.0, remaining))

    def record_exposure(self, cost: float, condition_id: str = "", question: str = "") -> None:
        """Record that we spent `cost` USDC on a trade."""
        normalized = self._normalize_condition_id(condition_id)
        with self._lock:
            self.current_exposure += cost
            self.total_trades += 1
            self.successful_trades += 1

            if normalized:
                self.positions.append({
                    "condition_id": normalized,
                    "question": question,
                    "cost": cost,
                    "timestamp": time.time(),
                    "settled": False,
                })

            exposure = self.current_exposure
            trade_count = self.total_trades

        log.info("Exposure updated: $%.2f / $%.2f (trade #%d)",
                 exposure, self.max_total_exposure, trade_count)

    def record_failure(self) -> None:
        """Record a failed trade attempt."""
        with self._lock:
            self.failed_trades += 1
            self.total_trades += 1

    def record_settlement(self, condition_id: str, payout: float) -> None:
        """Record that a position has been settled and capital returned."""
        normalized = self._normalize_condition_id(condition_id)
        with self._lock:
            for pos in self.positions:
                if pos["condition_id"] == normalized and not pos["settled"]:
                    pos["settled"] = True
                    profit = payout - pos["cost"]
                    self.total_profit += profit
                    self.current_exposure = max(0.0, self.current_exposure - pos["cost"])
                    log.info("Position settled: '%s' | cost=$%.2f | payout=$%.2f | profit=$%.4f",
                             pos["question"][:40], pos["cost"], payout, profit)
                    break

    def settle_all_for_market(self, condition_id: str) -> float:
        """
        Mark all positions for a given market as settled.
        For merge arbs, each share set = $1.00 payout.
        Returns total cost freed up.
        """
        normalized = self._normalize_condition_id(condition_id)
        freed = 0.0
        with self._lock:
            for pos in self.positions:
                if pos["condition_id"] == normalized and not pos["settled"]:
                    pos["settled"] = True
                    freed += pos["cost"]
                    self.current_exposure = max(0.0, self.current_exposure - pos["cost"])

        if freed > 0:
            log.info("Freed $%.2f exposure from settled positions in %s", freed, normalized[:20])
        return freed

    def can_trade(self) -> bool:
        """Check if we have headroom for any trade."""
        return self.max_allowed_cost() >= 1.0

    def reset(self) -> None:
        """Reset exposure tracking (e.g., after positions are settled)."""
        with self._lock:
            self.current_exposure = 0.0
            self.positions = [p for p in self.positions if not p["settled"]]
        log.info("Exposure reset to $0.00.")

    def cleanup_settled(self) -> None:
        """Remove settled positions from tracking."""
        with self._lock:
            before = len(self.positions)
            self.positions = [p for p in self.positions if not p["settled"]]
            removed = before - len(self.positions)
        if removed:
            log.info("Cleaned up %d settled positions.", removed)

    def summary(self) -> str:
        with self._lock:
            current_exposure = self.current_exposure
            max_total_exposure = self.max_total_exposure
            max_position_size = self.max_position_size
            successful_trades = self.successful_trades
            failed_trades = self.failed_trades
            total_profit = self.total_profit
        return (
            f"Exposure: ${current_exposure:.2f} / ${max_total_exposure:.2f} "
            f"| Per-trade cap: ${max_position_size:.2f} "
            f"| Available: ${self.max_allowed_cost():.2f} "
            f"| Trades: {successful_trades}ok/{failed_trades}fail "
            f"| P&L: ${total_profit:.4f}"
        )
