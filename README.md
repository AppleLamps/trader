# Polymarket Arbitrage Bot

Automated arbitrage detection and execution on [Polymarket](https://polymarket.com) prediction markets using the CLOB API.

## How It Works

The bot continuously:

1. **Fetches active markets** from the Polymarket Gamma API
2. **Scans orderbooks** for each market's outcomes via the CLOB API
3. **Detects arbitrage** — when buying all outcomes costs less than $1.00 (the guaranteed payout) after fees
4. **Executes trades** — buys all legs of a profitable arb (or logs in dry-run mode)

### Example Arbitrage

A binary Yes/No market where:

- Best ask for YES = $0.45
- Best ask for NO  = $0.50
- Fees (per-market) = $0.000
- **Total cost     = $0.950**
- **Profit         = $0.050 per share** (buy both -> guaranteed $1.00 payout)

## Setup

### 1. Install Python 3.11+

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Generate or Import a Wallet

**Option A — Generate a new wallet:**

```bash
python generate_wallet.py
```

Save the private key securely, then delete the script.

**Option B — Use an existing wallet (e.g. Phantom):**

Export your private key from Phantom (Settings -> Security -> Export Private Key). Convert it to hex format with `0x` prefix if needed.

### 4. Connect to Polymarket

1. Import your wallet into a browser extension (MetaMask, Phantom, Rabby, etc.)
2. Go to [polymarket.com](https://polymarket.com) and connect the wallet
3. Complete onboarding and deposit USDC
4. Find your **funder/proxy address**: click Deposit -> copy the deposit address (starts with `0x`)

### 5. Configure

Copy the example env file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env`:

- `PRIVATE_KEY` — Your wallet's private key (hex, 0x-prefixed)
- `FUNDER_ADDRESS` — Your Polymarket proxy/deposit address (from the Deposit page)
- Adjust strategy parameters as needed

**Security**: Never commit `.env`. The `.gitignore` already excludes it.

### 6. Verify Connection

```bash
python test_connection.py
```

This checks that your key, funder address, and API auth all work. It also fetches a sample orderbook.

### 7. Check Balances

```bash
python check_balance.py     # CLOB trading balance (collateral)
python check_onchain.py     # On-chain USDC/POL balance at FUNDER_ADDRESS
```

### 8. Run (Dry Run first!)

```bash
python bot.py
```

By default, `DRY_RUN=true` -- the bot will scan and log opportunities without placing real orders. Once you're comfortable, set `DRY_RUN=false` in `.env` to enable live trading.

## Configuration Reference

| Variable | Default | Description |
|---|---|---|
| `PRIVATE_KEY` | — | Your wallet private key |
| `FUNDER_ADDRESS` | — | Polymarket funder/proxy address |
| `CLOB_HOST` | `https://clob.polymarket.com` | CLOB API endpoint |
| `CHAIN_ID` | `137` | Polygon mainnet |
| `MIN_PROFIT_MARGIN` | `0.005` | Min profit per share to trigger arb ($) |
| `MAX_POSITION_SIZE` | `10.0` | Max USDC per single trade |
| `MAX_TOTAL_EXPOSURE` | `100.0` | Max total USDC across all positions |
| `SCAN_INTERVAL` | `10` | Seconds between scans |
| `MIN_BOOK_DEPTH` | `5` | Min shares on ask side to consider |
| `DRY_RUN` | `true` | Log-only mode (no real trades) |
| `LOG_LEVEL` | `INFO` | DEBUG/INFO/WARNING/ERROR |
| `MIN_COST_THRESHOLD` | `0.90` | Skip arbs with total cost below this |
| `MAX_PROFIT_PER_SHARE` | `0.05` | Skip arbs with profit/share above this |
| `MIN_ARB_VALUE` | `0.50` | Skip arbs with estimated profit below this |
| `MIN_MARKET_LIQUIDITY` | `1000` | Gamma liquidity filter |
| `WS_ENABLED` | `true` | Use WebSocket mode |
| `WS_HOST` | `wss://ws-subscriptions-clob.polymarket.com/ws/market` | WebSocket host |
| `HEARTBEAT_ENABLED` | `true` | Dead-man switch on/off |
| `HEARTBEAT_INTERVAL` | `5` | Heartbeat interval (seconds) |
| `USE_FOK_ORDERS` | `true` | Fill-or-kill orders |
| `USE_BATCH_ORDERS` | `true` | Submit all legs at once |
| `GTD_EXPIRY_SECONDS` | `30` | GTD expiry (0 = GTC) |
| `REQUIRE_FULL_MATCH` | `true` | Require every leg to be immediately matched |
| `BALANCE_CHECK_ENABLED` | `true` | Block trades if balance low |

## Project Structure

```
├── bot.py              — Main loop (entry point)
├── config.py           — Loads .env settings
├── client.py           — Polymarket CLOB client wrapper
├── markets.py          — Market discovery via Gamma API
├── arbitrage.py        — Arbitrage detection engine
├── executor.py         — Trade execution with safety checks
├── risk.py             — Position/exposure limits
├── logger.py           — Logging setup
├── generate_wallet.py  — One-time wallet generator (delete after use)
├── test_connection.py  — Verify API credentials & connectivity
├── check_balance.py    — Check CLOB trading balance
├── check_onchain.py    — Check on-chain USDC/POL balances
├── derive_funder.py    — Derive funder address from private key
├── requirements.txt
├── .env.example        — Config template
└── .gitignore
```

## Risks & Warnings

- **You can lose money.** Arbitrage on prediction markets is competitive — opportunities are rare and fleeting. Slippage, partial fills, and timing can turn a theoretical profit into a loss.
- **Start with `DRY_RUN=true`** and tiny position sizes.
- **Never expose your private key.** Use env vars only, never hardcode.
- **This is not financial advice.** Use at your own risk.

## Wallet and Funder Address

Polymarket uses two addresses:

- **Signer EOA**: derived from your `PRIVATE_KEY`. This signs orders.
- **Funder/Proxy**: shown on the Polymarket Deposit page. This holds funds.

These must belong to the same Polymarket account. If they do not match, you will see
`invalid signature` errors when placing orders.

Quick check:

```bash
python derive_funder.py
```

Compare the printed **Signer EOA** with the wallet you connect on Polymarket and make sure
the **Funder (env)** address matches the Deposit/Proxy address for that same wallet.
