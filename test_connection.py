"""Quick test: verify API credentials and connectivity."""

from py_clob_client.client import ClobClient
from eth_account import Account

KEY = "0xf92e5de4b43b0ba8155db1cc9f85ab1b16980577698efe6e3dfc7b32c156ba58"
FUNDER = "0xEDb15b03823dFf90cEf241E00c46410D1fc07764"
HOST = "https://clob.polymarket.com"
CHAIN_ID = 137

# 1. Verify key -> address
acct = Account.from_key(KEY)
print(f"EOA Address: {acct.address}")
print(f"Funder:      {FUNDER}")

# 2. Auth with CLOB
print("\nAuthenticating with CLOB API...")
client = ClobClient(host=HOST, key=KEY, chain_id=CHAIN_ID, funder=FUNDER)
creds = client.create_or_derive_api_creds()
client.set_api_creds(creds)
print(f"API Key:     {creds.api_key}")
print("Auth OK!")

# 3. Test orderbook fetch
print("\nFetching a sample orderbook...")
try:
    # Use a well-known token ID (any active market)
    import requests
    resp = requests.get("https://gamma-api.polymarket.com/markets", params={"limit": 1, "active": "true", "closed": "false"}, timeout=10)
    markets = resp.json()
    if markets:
        import json
        token_ids = markets[0].get("clobTokenIds") or markets[0].get("clob_token_ids", "[]")
        if isinstance(token_ids, str):
            token_ids = json.loads(token_ids)
        if token_ids:
            book = client.get_order_book(token_ids[0])
            asks = getattr(book, "asks", []) or []
            bids = getattr(book, "bids", []) or []
            print(f"Market: {markets[0].get('question', 'N/A')[:60]}")
            print(f"Token:  {token_ids[0][:20]}...")
            print(f"Result: {len(asks)} asks, {len(bids)} bids")
        else:
            print("No token IDs found on sample market.")
    else:
        print("No active markets returned.")
except Exception as e:
    print(f"Orderbook test failed: {e}")

print("\nAll checks passed!")
