import unittest

from arbitrage import scan_all_markets, scan_market_for_arb
from markets import Market, MarketOutcome


class FakePoly:
    @staticmethod
    def get_best_ask(order_book):
        # In tests we pass (price, size) tuples as synthetic orderbooks.
        if isinstance(order_book, tuple) and len(order_book) == 2:
            return order_book
        return None

    @staticmethod
    def get_fee_rate_bps(_token_id: str) -> int:
        return 0

    @staticmethod
    def get_order_books_batch(_token_ids):
        return []


def make_binary_market(condition_id: str, question: str, yes_token: str, no_token: str) -> Market:
    return Market(
        condition_id=condition_id,
        question=question,
        slug=question.lower().replace(" ", "-"),
        active=True,
        closed=False,
        outcomes=[
            MarketOutcome(token_id=yes_token, outcome="Yes"),
            MarketOutcome(token_id=no_token, outcome="No"),
        ],
        volume=0.0,
        liquidity=0.0,
    )


class OpportunityRankingTests(unittest.TestCase):
    def test_low_fill_confidence_is_filtered(self):
        poly = FakePoly()
        market = make_binary_market("m1", "Low depth market", "yes1", "no1")
        orderbooks = {
            "yes1": (0.45, 10.0),
            "no1": (0.50, 10.0),
        }
        opp = scan_market_for_arb(
            poly=poly,
            market=market,
            orderbooks=orderbooks,
            min_profit=0.005,
            min_depth=20.0,
            min_arb_value=0.1,
            min_roi=0.0,
            min_fill_confidence=0.50,  # strict confidence floor
        )
        self.assertIsNone(opp)

    def test_opportunities_rank_by_priority_score_not_raw_profit(self):
        poly = FakePoly()
        market_high_roi = make_binary_market("m2", "High ROI", "yes2", "no2")
        market_low_roi_big_size = make_binary_market("m3", "Low ROI bigger size", "yes3", "no3")
        preloaded = {
            # High ROI (~4.93%), moderate absolute profit
            "yes2": (0.463, 80.0),
            "no2": (0.49, 80.0),
            # Lower ROI (~2.04%), larger absolute profit
            "yes3": (0.48, 300.0),
            "no3": (0.50, 300.0),
        }

        opps = scan_all_markets(
            poly=poly,
            markets=[market_low_roi_big_size, market_high_roi],
            min_profit=0.005,
            min_depth=20.0,
            min_arb_value=0.1,
            min_cost_threshold=0.90,
            max_profit_per_share=0.05,
            min_roi=0.0,
            min_fill_confidence=0.0,
            preloaded_orderbooks=preloaded,
            fetch_missing_orderbooks=False,
        )
        self.assertGreaterEqual(len(opps), 2)
        self.assertEqual(opps[0].market.question, "High ROI")
        self.assertGreater(opps[0].priority_score, opps[1].priority_score)


if __name__ == "__main__":
    unittest.main()
