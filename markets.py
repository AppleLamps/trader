"""
Market discovery — fetches active markets from the Polymarket Gamma API
and structures them for the arbitrage scanner.

Pre-filters markets using Gamma's reported outcome prices to skip obviously
non-arbitrageable markets before making expensive CLOB orderbook calls.
"""

import json
import logging
from dataclasses import dataclass, field
import requests

log = logging.getLogger("polyarb.markets")

GAMMA_API = "https://gamma-api.polymarket.com"


@dataclass
class MarketOutcome:
    """A single outcome token within a market."""
    token_id: str
    outcome: str  # e.g. "Yes", "No", or named outcome
    price: float | None = None  # last traded / mid price from Gamma


@dataclass
class Market:
    """A Polymarket event market (condition)."""
    condition_id: str
    question: str
    slug: str
    active: bool
    closed: bool
    outcomes: list[MarketOutcome] = field(default_factory=list)
    volume: float = 0.0
    liquidity: float = 0.0


def fetch_active_markets(
    limit: int = 100,
    min_liquidity: float = 0,
    price_sum_threshold: float = 1.05,
) -> list[Market]:
    """
    Fetch active, open markets from Gamma API.
    
    Pre-filters using Gamma's outcome prices: only markets where the sum of
    outcome prices is below `price_sum_threshold` are returned, since those
    are the only ones that could possibly be arbitrageable after checking
    the real orderbook. This avoids expensive CLOB calls for the ~90% of
    markets that obviously sum to ~1.0.
    
    Returns a list of Market objects with their outcome token IDs.
    """
    markets: list[Market] = []
    skipped = 0
    offset = 0

    while len(markets) < limit:
        params = {
            "limit": min(100, limit - len(markets) + 50),  # overfetch to compensate for filtering
            "offset": offset,
            "active": "true",
            "closed": "false",
        }
        try:
            resp = requests.get(f"{GAMMA_API}/markets", params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            log.error("Gamma API request failed: %s", e)
            break

        if not data:
            break

        for item in data:
            token_ids = item.get("clobTokenIds") or item.get("clob_token_ids")
            outcome_names = item.get("outcomes")
            outcome_prices = item.get("outcomePrices") or item.get("outcome_prices")

            if not token_ids or not outcome_names:
                continue

            if isinstance(token_ids, str):
                token_ids = json.loads(token_ids)
            if isinstance(outcome_names, str):
                outcome_names = json.loads(outcome_names)
            if isinstance(outcome_prices, str):
                outcome_prices = json.loads(outcome_prices)

            liq = float(item.get("liquidity", 0) or 0)
            if liq < min_liquidity:
                continue

            # Pre-filter: check if Gamma's prices suggest a possible arb
            prices = []
            if outcome_prices:
                for p in outcome_prices:
                    try:
                        prices.append(float(p))
                    except (ValueError, TypeError):
                        prices = []
                        break

            if prices and len(prices) == len(token_ids):
                price_sum = sum(prices)
                if price_sum > price_sum_threshold:
                    skipped += 1
                    continue

            outcomes = []
            for i, tid in enumerate(token_ids):
                name = outcome_names[i] if i < len(outcome_names) else f"Outcome {i}"
                price = prices[i] if i < len(prices) else None
                outcomes.append(MarketOutcome(token_id=tid, outcome=name, price=price))

            market = Market(
                condition_id=item.get("conditionId") or item.get("condition_id", ""),
                question=item.get("question", ""),
                slug=item.get("slug", ""),
                active=bool(item.get("active", True)),
                closed=bool(item.get("closed", False)),
                outcomes=outcomes,
                volume=float(item.get("volume", 0) or 0),
                liquidity=liq,
            )
            markets.append(market)

            if len(markets) >= limit:
                break

        offset += len(data)
        if len(data) < 100:
            break

    log.info("Fetched %d candidate markets (%d skipped by price pre-filter).", len(markets), skipped)
    return markets
