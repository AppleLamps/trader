"""Check USDC balance on Polymarket."""

from py_clob_client.client import ClobClient
from py_clob_client.clob_types import BalanceAllowanceParams, AssetType

KEY = "0xf92e5de4b43b0ba8155db1cc9f85ab1b16980577698efe6e3dfc7b32c156ba58"
FUNDER = "0x003D2F5Fc0a0E6018DD30Cf137cC85a4a3718c5d"

client = ClobClient(host="https://clob.polymarket.com", key=KEY, chain_id=137, funder=FUNDER)
creds = client.create_or_derive_api_creds()
client.set_api_creds(creds)

params = BalanceAllowanceParams(asset_type=AssetType.COLLATERAL)
result = client.get_balance_allowance(params)
print(f"USDC Balance:   {result}")
