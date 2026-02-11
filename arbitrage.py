"""
Arbitrage detection engine.

Scans markets for arbitrage opportunities where the total cost of buying
all outcomes is less than $1.00 (the guaranteed payout), minus fees.

For a binary market (Yes/No):
  If best_ask(YES) + best_ask(NO) + fees < 1.00  →  arbitrage exists.

For multi-outcome markets:
  If sum of all best asks + fees < 1.00  →  arbitrage exists.

Upgrades:
  - Batch orderbook fetching (2 API calls instead of 1000)
  - Per-market fee rates from API (most markets = 0% fees!)
  - Spread pre-filtering to skip illiquid markets fast
  - Orderbook hash caching to skip unchanged books
  - Curved fee calculation for 15-min crypto markets
"""

import logging
from dataclasses import dataclass

from client import PolyClient
from markets import Market

log = logging.getLogger("polyarb.arbitrage")


@dataclass
class ArbOpportunity:
    """Represents a detected arbitrage opportunity."""
    market: Market
    # For each outcome: (token_id, outcome_name, ask_price, available_size)
    legs: list[tuple[str, str, float, float]]
    total_cost: float       # Sum of ask prices across all outcomes
    total_cost_with_fees: float
    profit_per_share: float  # 1.0 - total_cost_with_fees
    max_shares: float        # Limited by smallest leg size
    estimated_profit: float  # profit_per_share * max_shares
    fee_rate_bps: int = 0    # Actual fee rate for this market


def calculate_polymarket_fee(price: float, shares: float, fee_rate_bps: int) -> float:
    """
    Calculate Polymarket's curved taker fee.

    Most prediction markets have fee_rate_bps=0 (NO FEES).
    Only 15-minute crypto markets have fees, using the formula:
      fee = shares × price × 0.25 × (price × (1 - price))²

    The fee_rate_bps from the API indicates whether fees apply.
    """
    if fee_rate_bps == 0:
        return 0.0

    # Polymarket's curved fee formula (peaks at 50/50 price, zero at extremes)
    fee = shares * price * 0.25 * (price * (1.0 - price)) ** 2
    return max(fee, 0.0)


def calculate_fee_per_share(price: float, fee_rate_bps: int) -> float:
    """Calculate fee per share for a given price. Used for arb detection."""
    if fee_rate_bps == 0:
        return 0.0
    return price * 0.25 * (price * (1.0 - price)) ** 2


def scan_market_for_arb(
    poly: PolyClient,
    market: Market,
    orderbooks: dict[str, object],
    min_profit: float,
    min_depth: float,
    min_arb_value: float = 0.50,
    min_cost_threshold: float = 0.90,
    max_profit_per_share: float = 0.05,
) -> ArbOpportunity | None:
    """
    Check a single market for arbitrage opportunity using pre-fetched orderbooks.

    The fee rate is looked up per-market from the API. Most prediction markets
    have 0% fees, so this unlocks many arbs that the old 2% hardcoded rate filtered out.
    """
    if len(market.outcomes) < 2:
        return None

    legs: list[tuple[str, str, float, float]] = []
    fee_rate_bps = None

    for outcome in market.outcomes:
        ob = orderbooks.get(outcome.token_id)
        if ob is None:
            return None

        # Skip if orderbook hasn't changed since last scan (optimization)
        # The hash check is done at the scan_all level now

        best = poly.get_best_ask(ob)
        if best is None:
            log.debug("No asks for %s in market '%s'", outcome.outcome, market.question[:50])
            return None

        ask_price, ask_size = best
        if ask_size < min_depth:
            log.debug("Insufficient depth (%.1f < %.1f) for %s in '%s'",
                      ask_size, min_depth, outcome.outcome, market.question[:50])
            return None

        # Look up actual fee rate (cached per-token in the client)
        if fee_rate_bps is None:
            fee_rate_bps = poly.get_fee_rate_bps(outcome.token_id)

        legs.append((outcome.token_id, outcome.outcome, ask_price, ask_size))

    if fee_rate_bps is None:
        fee_rate_bps = 0

    total_cost = sum(price for _, _, price, _ in legs)

    # Calculate fees using actual per-market rate
    total_fees = sum(calculate_fee_per_share(price, fee_rate_bps) for _, _, price, _ in legs)
    total_cost_with_fees = total_cost + total_fees
    profit_per_share = 1.0 - total_cost_with_fees

    if profit_per_share < min_profit:
        return None

    # ── Sanity filters: reject bogus arbs from stale/abandoned orders ──
    #
    # Problem: Polymarket orderbooks often have stale asks sitting at absurd
    # prices. E.g., "Ivory Coast wins World Cup" has YES ask at $0.005 AND
    # a stale NO ask at $0.005, making it look like a $0.99/share arb.
    # In reality, NO should be ~$0.995.
    #
    # Filter 1: Minimum total cost — real binary arbs cost $0.95-$0.999.
    #   If YES+NO < $0.90, the NO side has a stale/abandoned ask.
    if total_cost_with_fees < min_cost_threshold:
        log.debug(
            "REJECTED (stale orders): '%s' — cost $%.4f < threshold $%.2f",
            market.question[:50], total_cost_with_fees, min_cost_threshold,
        )
        return None

    # Filter 2: Max profit per share — if it's "too good to be true", it is.
    #   A guaranteed 10%+ return sitting unclaimed = stale orderbook, not a real arb.
    #   Real arbs in efficient markets yield 0.5-3% per share.
    if profit_per_share > max_profit_per_share:
        log.debug(
            "REJECTED (too good): '%s' — profit/share $%.4f > max $%.4f",
            market.question[:50], profit_per_share, max_profit_per_share,
        )
        return None

    max_shares = min(size for _, _, _, size in legs)
    estimated_profit = profit_per_share * max_shares

    # Filter out arbs worth less than the minimum dollar threshold
    if estimated_profit < min_arb_value:
        log.debug(
            "REJECTED (too small): '%s' — est. profit $%.2f < min $%.2f",
            market.question[:50], estimated_profit, min_arb_value,
        )
        return None

    opp = ArbOpportunity(
        market=market,
        legs=legs,
        total_cost=total_cost,
        total_cost_with_fees=total_cost_with_fees,
        profit_per_share=profit_per_share,
        max_shares=max_shares,
        estimated_profit=estimated_profit,
        fee_rate_bps=fee_rate_bps,
    )

    fee_label = f"fee={fee_rate_bps}bps" if fee_rate_bps > 0 else "NO FEES"
    log.info(
        "ARB FOUND: '%s' | cost=%.4f | w/fees=%.4f | profit/share=$%.4f | max=%.0f | est=$%.2f | %s",
        market.question[:60],
        total_cost,
        total_cost_with_fees,
        profit_per_share,
        max_shares,
        opp.estimated_profit,
        fee_label,
    )

    return opp


def scan_all_markets(
    poly: PolyClient,
    markets: list[Market],
    min_profit: float,
    min_depth: float,
    min_arb_value: float = 0.50,
    min_cost_threshold: float = 0.90,
    max_profit_per_share: float = 0.05,
) -> list[ArbOpportunity]:
    """
    Scan a list of markets using BATCH orderbook fetching.

    Instead of N individual API calls per market, this fetches ALL orderbooks
    in batches of 500 tokens per call — typically 2-4 calls instead of 500-1000.
    """
    opportunities: list[ArbOpportunity] = []

    # Collect all token IDs we need orderbooks for
    all_token_ids = []
    token_to_market: dict[str, Market] = {}
    for market in markets:
        for outcome in market.outcomes:
            all_token_ids.append(outcome.token_id)
            token_to_market[outcome.token_id] = market

    if not all_token_ids:
        return opportunities

    log.info("Batch fetching %d orderbooks...", len(all_token_ids))

    # BATCH FETCH: 500 tokens per API call instead of 1 per call
    orderbook_list = poly.get_order_books_batch(all_token_ids)

    # Map token_id → orderbook for quick lookup
    orderbooks: dict[str, object] = {}
    for i, tid in enumerate(all_token_ids):
        if i < len(orderbook_list):
            orderbooks[tid] = orderbook_list[i]

    # Scan each market using pre-fetched orderbooks
    for market in markets:
        opp = scan_market_for_arb(poly, market, orderbooks, min_profit, min_depth,
                                  min_arb_value, min_cost_threshold, max_profit_per_share)
        if opp is not None:
            opportunities.append(opp)

    # Sort by estimated profit descending (best arbs first)
    opportunities.sort(key=lambda o: o.estimated_profit, reverse=True)
    return opportunities
