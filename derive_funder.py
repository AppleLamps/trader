"""
Print Polymarket addresses for debugging invalid signature errors.
"""

import os

from dotenv import load_dotenv
from eth_account import Account
from py_clob_client.client import ClobClient

HOST = "https://clob.polymarket.com"
CHAIN_ID = 137

load_dotenv()

PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")
FUNDER_ADDRESS = os.getenv("FUNDER_ADDRESS", "")

if not PRIVATE_KEY:
    raise SystemExit("Missing PRIVATE_KEY in .env")

client = ClobClient(host=HOST, key=PRIVATE_KEY, chain_id=CHAIN_ID, funder=FUNDER_ADDRESS or None)

print("Deriving API credentials...")
creds = client.create_or_derive_api_creds()
print(f"API Key:        {creds.api_key}")
print(f"API Secret:     {creds.api_secret}")
print(f"API Passphrase: {creds.api_passphrase}")

acct = Account.from_key(PRIVATE_KEY)
print(f"Signer EOA:     {acct.address}")
print(f"Funder (env):   {FUNDER_ADDRESS or '(not set)'}")

if FUNDER_ADDRESS:
    print("Note: If funder does not match the deposit/proxy address for this EOA,")
    print("orders will fail with 'invalid signature'.")
