"""Quick test: verify API credentials and connectivity."""

from eth_account import Account

from client import PolyClient
from config import load_config
from markets import fetch_active_markets


def main() -> None:
    cfg = load_config()
    account = Account.from_key(cfg.private_key)

    print(f"EOA Address: {account.address}")
    print(f"Funder:      {cfg.funder_address}")

    print("\nAuthenticating with CLOB API...")
    poly = PolyClient(cfg)
    poly.authenticate()
    print("Auth OK!")

    print("\nChecking CLOB health...")
    if not poly.is_server_up():
        raise SystemExit("CLOB API health check failed.")
    print("CLOB server: OK")

    print("\nFetching a sample orderbook...")
    markets = fetch_active_markets(limit=1)
    if not markets or not markets[0].outcomes:
        raise SystemExit("No active market with outcomes was returned.")

    market = markets[0]
    token_id = market.outcomes[0].token_id
    order_book = poly.get_order_book(token_id)
    asks = getattr(order_book, "asks", []) or []
    bids = getattr(order_book, "bids", []) or []

    print(f"Market: {market.question[:60]}")
    print(f"Token:  {token_id[:20]}...")
    print(f"Result: {len(asks)} asks, {len(bids)} bids")
    print("\nAll checks passed!")


if __name__ == "__main__":
    main()
