"""Check USDC balances available for trading."""

from client import PolyClient
from config import load_config


def main() -> None:
    cfg = load_config()
    poly = PolyClient(cfg)
    poly.authenticate()

    clob_balance = poly.get_usdc_balance()
    wallet_balance = poly.get_onchain_usdc_balance(use_cache=False)
    available = max(clob_balance, wallet_balance)

    print("USDC balances")
    print(f"  CLOB collateral: ${clob_balance:.2f}")
    print(f"  Wallet on-chain: ${wallet_balance:.2f}")
    print(f"  Max spendable now: ${available:.2f}")


if __name__ == "__main__":
    main()
