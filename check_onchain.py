"""Check USDC balance on Polygon for both EOA and funder addresses."""

import requests

USDC_CONTRACT = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"  # USDC on Polygon
USDC_V2 = "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359"  # USDC native on Polygon

EOA = "0x52F74b5663482C4e40C8C87EcDeaE0CBFcd06D91"
FUNDER = "0xEDb15b03823dFf90cEf241E00c46410D1fc07764"

def check_usdc_balance(address, label, usdc_addr):
    # ERC-20 balanceOf(address) selector = 0x70a08231
    data = "0x70a08231" + address[2:].lower().zfill(64)
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [{"to": usdc_addr, "data": data}, "latest"],
        "id": 1,
    }
    resp = requests.post("https://polygon-rpc.com", json=payload, timeout=10)
    result = resp.json().get("result", "0x0")
    balance = int(result, 16) / 1e6  # USDC has 6 decimals
    return balance

for label, addr in [("EOA (Phantom)", EOA), ("Funder (Polymarket proxy)", FUNDER)]:
    b1 = check_usdc_balance(addr, label, USDC_CONTRACT)
    b2 = check_usdc_balance(addr, label, USDC_V2)
    print(f"{label}: {addr}")
    print(f"  USDC.e balance: ${b1:.2f}")
    print(f"  USDC   balance: ${b2:.2f}")
    print()

# Also check MATIC/POL balance
for label, addr in [("EOA (Phantom)", EOA), ("Funder (Polymarket proxy)", FUNDER)]:
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [addr, "latest"],
        "id": 1,
    }
    resp = requests.post("https://polygon-rpc.com", json=payload, timeout=10)
    result = resp.json().get("result", "0x0")
    balance = int(result, 16) / 1e18
    print(f"{label} POL/MATIC: {balance:.4f}")
