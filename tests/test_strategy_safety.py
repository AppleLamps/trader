import unittest
from types import SimpleNamespace

from arbitrage import ArbOpportunity, calculate_fee_per_share
from executor import Executor
from markets import Market
from risk import RiskManager


def make_config(**overrides):
    values = {
        "private_key": "0xabc",
        "funder_address": "0xdef",
        "clob_host": "https://clob.polymarket.com",
        "chain_id": 137,
        "builder_api_key": "",
        "builder_secret": "",
        "builder_passphrase": "",
        "min_profit_margin": 0.005,
        "max_position_size": 50.0,
        "max_total_exposure": 500.0,
        "scan_interval": 10,
        "min_book_depth": 20.0,
        "dry_run": False,
        "log_level": "INFO",
        "min_cost_threshold": 0.90,
        "max_profit_per_share": 0.05,
        "min_arb_value": 0.50,
        "min_market_liquidity": 1000.0,
        "ws_enabled": True,
        "ws_host": "wss://ws-subscriptions-clob.polymarket.com/ws/market",
        "heartbeat_enabled": False,
        "heartbeat_interval": 5,
        "use_fok_orders": True,
        "use_batch_orders": True,
        "gtd_expiry_seconds": 30,
        "require_full_match": True,
        "balance_check_enabled": False,
    }
    values.update(overrides)
    return SimpleNamespace(**values)


def make_opportunity(condition_id: str = "abcd1234") -> ArbOpportunity:
    market = Market(
        condition_id=condition_id,
        question="Will test pass?",
        slug="test-market",
        active=True,
        closed=False,
        outcomes=[],
        volume=0.0,
        liquidity=0.0,
    )
    return ArbOpportunity(
        market=market,
        legs=[
            ("token_yes", "Yes", 0.45, 25.0),
            ("token_no", "No", 0.50, 25.0),
        ],
        total_cost=0.95,
        total_cost_with_fees=0.95,
        profit_per_share=0.05,
        max_shares=10.0,
        estimated_profit=0.50,
        fee_rate_bps=0,
    )


class FakePoly:
    def __init__(self, batch_response):
        self._batch_response = batch_response
        self.cancel_called = False

    def get_usdc_balance(self):
        return 10_000.0

    def get_onchain_usdc_balance(self):
        return 10_000.0

    def get_server_time(self):
        return 1_700_000_000

    def place_batch_orders(self, _orders):
        return self._batch_response

    def cancel_all_orders(self):
        self.cancel_called = True
        return {"canceled": "all"}


class StrategySafetyTests(unittest.TestCase):
    def test_fee_curve_scales_with_fee_rate(self):
        fee_full = calculate_fee_per_share(0.5, 1000)
        fee_half = calculate_fee_per_share(0.5, 500)
        self.assertGreater(fee_full, 0.0)
        self.assertAlmostEqual(fee_half, fee_full / 2.0, places=8)

    def test_batch_requires_immediate_match(self):
        cfg = make_config(require_full_match=True)
        risk = RiskManager(cfg)
        poly = FakePoly(
            [
                {"success": True, "errorMsg": "", "orderID": "1", "status": "matched"},
                {"success": True, "errorMsg": "", "orderID": "2", "status": "live"},
            ]
        )
        executor = Executor(poly=poly, risk=risk, cfg=cfg, dry_run=False)
        ok = executor.execute_arb(make_opportunity())

        self.assertFalse(ok)
        self.assertTrue(poly.cancel_called)
        self.assertEqual(risk.current_exposure, 0.0)
        self.assertEqual(risk.failed_trades, 1)

    def test_successful_trade_records_settleable_position(self):
        cfg = make_config(require_full_match=True)
        risk = RiskManager(cfg)
        poly = FakePoly(
            [
                {"success": True, "errorMsg": "", "orderID": "1", "status": "matched"},
                {"success": True, "errorMsg": "", "orderID": "2", "status": "matched"},
            ]
        )
        executor = Executor(poly=poly, risk=risk, cfg=cfg, dry_run=False)
        opp = make_opportunity(condition_id="abcd1234")
        ok = executor.execute_arb(opp)

        self.assertTrue(ok)
        self.assertGreater(risk.current_exposure, 0.0)
        self.assertEqual(len(risk.positions), 1)

        # settlement event may include "0x" prefix; normalization should still match
        freed = risk.settle_all_for_market("0xabcd1234")
        self.assertGreater(freed, 0.0)
        self.assertEqual(risk.current_exposure, 0.0)


if __name__ == "__main__":
    unittest.main()
