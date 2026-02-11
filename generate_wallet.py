"""
Generate a new Ethereum wallet (private key + address).
Run once, save the output securely, then delete this script.
"""

from eth_account import Account


def main():
    acct = Account.create()
    print("=" * 60)
    print("  NEW ETHEREUM WALLET")
    print("=" * 60)
    print(f"  Address:     {acct.address}")
    print(f"  Private Key: {acct.key.hex()}")
    print("=" * 60)
    print()
    print("IMPORTANT:")
    print("  1. Copy the private key and store it somewhere SAFE.")
    print("  2. Put the private key in your .env as PRIVATE_KEY=0x...")
    print("  3. NEVER share the private key with anyone.")
    print("  4. Delete this script after use.")
    print()
    print("NEXT STEPS:")
    print("  - Fund this wallet with USDC on Polygon.")
    print("  - You also need a small amount of MATIC for gas.")
    print("  - Go to https://polymarket.com, connect this wallet,")
    print("    and complete any required onboarding/deposit.")
    print("  - Your FUNDER_ADDRESS (Polymarket proxy wallet)")
    print("    will be shown in Polymarket Settings after connecting.")


if __name__ == "__main__":
    main()
