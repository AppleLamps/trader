"""Check on-chain balances for signer and funder addresses."""

import requests
from eth_account import Account

from config import load_config

RPC_URL = "https://polygon-rpc.com"
USDC_E = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"  # Bridged USDC.e
USDC_NATIVE = "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359"  # Native USDC


def _rpc_call(session: requests.Session, method: str, params: list) -> dict:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params,
    }
    response = session.post(RPC_URL, json=payload, timeout=10)
    response.raise_for_status()
    return response.json()


def _erc20_balance(session: requests.Session, token_address: str, wallet_address: str) -> float:
    # ERC-20 balanceOf(address) selector = 0x70a08231
    data = "0x70a08231" + wallet_address[2:].lower().zfill(64)
    result = _rpc_call(
        session,
        "eth_call",
        [{"to": token_address, "data": data}, "latest"],
    ).get("result", "0x0")
    return int(result, 16) / 1e6


def _native_balance(session: requests.Session, wallet_address: str) -> float:
    result = _rpc_call(
        session,
        "eth_getBalance",
        [wallet_address, "latest"],
    ).get("result", "0x0")
    return int(result, 16) / 1e18


def main() -> None:
    cfg = load_config()
    signer = Account.from_key(cfg.private_key).address
    addresses = [
        ("Signer EOA", signer),
        ("Funder (proxy)", cfg.funder_address),
    ]

    with requests.Session() as session:
        for label, address in addresses:
            usdc_e_balance = _erc20_balance(session, USDC_E, address)
            usdc_native_balance = _erc20_balance(session, USDC_NATIVE, address)
            pol_balance = _native_balance(session, address)

            print(f"{label}: {address}")
            print(f"  USDC.e balance: ${usdc_e_balance:.2f}")
            print(f"  USDC   balance: ${usdc_native_balance:.2f}")
            print(f"  POL/MATIC balance: {pol_balance:.4f}")
            print()


if __name__ == "__main__":
    main()
