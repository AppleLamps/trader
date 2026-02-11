---
url: "https://docs.polymarket.com/developers/market-makers/maker-rebates-program"
title: "Maker Rebates Program - Polymarket Documentation"
---

[Skip to main content](https://docs.polymarket.com/developers/market-makers/maker-rebates-program#content-area)

[Polymarket Documentation home page![light logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-black.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=aff81820f1f3d577fecb3956a8a3bee1)![dark logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-white.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=3bc6857b5dbe8b74b9a7d40975c19b2b)](https://docs.polymarket.com/)

Search...

Ctrl K

Search...

Navigation

Market Makers

Maker Rebates Program

[User Guide](https://docs.polymarket.com/polymarket-learn/get-started/what-is-polymarket) [For Developers](https://docs.polymarket.com/quickstart/overview) [Changelog](https://docs.polymarket.com/changelog/changelog)

On this page

- [Fee Handling by Implementation Type](https://docs.polymarket.com/developers/market-makers/maker-rebates-program#fee-handling-by-implementation-type)
- [Option 1: Official CLOB Clients (Recommended)](https://docs.polymarket.com/developers/market-makers/maker-rebates-program#option-1-official-clob-clients-recommended)
- [Option 2: REST API / Custom Implementations](https://docs.polymarket.com/developers/market-makers/maker-rebates-program#option-2-rest-api-%2F-custom-implementations)
- [Step 1: Fetch the Fee Rate](https://docs.polymarket.com/developers/market-makers/maker-rebates-program#step-1-fetch-the-fee-rate)
- [Step 2: Include in Your Signed Order](https://docs.polymarket.com/developers/market-makers/maker-rebates-program#step-2-include-in-your-signed-order)
- [Step 3: Sign and Submit](https://docs.polymarket.com/developers/market-makers/maker-rebates-program#step-3-sign-and-submit)
- [Fee Behavior](https://docs.polymarket.com/developers/market-makers/maker-rebates-program#fee-behavior)
- [Fee Table (100 shares)](https://docs.polymarket.com/developers/market-makers/maker-rebates-program#fee-table-100-shares)
- [Maker Rebates](https://docs.polymarket.com/developers/market-makers/maker-rebates-program#maker-rebates)
- [How Rebates Work](https://docs.polymarket.com/developers/market-makers/maker-rebates-program#how-rebates-work)
- [Rebate Pool](https://docs.polymarket.com/developers/market-makers/maker-rebates-program#rebate-pool)
- [Which Markets Have Fees?](https://docs.polymarket.com/developers/market-makers/maker-rebates-program#which-markets-have-fees)
- [Related Documentation](https://docs.polymarket.com/developers/market-makers/maker-rebates-program#related-documentation)

Polymarket has enabled **taker fees** on **15-minute crypto markets**. These fees fund a **Maker Rebates** program that pays daily USDC rebates to liquidity providers.

## [​](https://docs.polymarket.com/developers/market-makers/maker-rebates-program\#fee-handling-by-implementation-type)  Fee Handling by Implementation Type

### [​](https://docs.polymarket.com/developers/market-makers/maker-rebates-program\#option-1-official-clob-clients-recommended)  Option 1: Official CLOB Clients (Recommended)

The official CLOB clients **automatically handle fees** for you. Update to the latest version: [**TypeScript Client** \\
\\
npm install @polymarket/clob-client@latest](https://github.com/Polymarket/clob-client)

[**Python Client** \\
\\
pip install —upgrade py-clob-client](https://github.com/Polymarket/py-clob-client) [**Rust Client** \\
\\
cargo add polymarket-client-sdk](https://github.com/Polymarket/rs-clob-client)

**What the client does automatically:**

1. Fetches the fee rate for the market’s token ID
2. Includes `feeRateBps` in the order structure
3. Signs the order with the fee rate included

**You don’t need to do anything extra**. Just update your client and your orders will work on fee-enabled markets.

* * *

### [​](https://docs.polymarket.com/developers/market-makers/maker-rebates-program\#option-2-rest-api-/-custom-implementations)  Option 2: REST API / Custom Implementations

If you’re calling the REST API directly or building your own order signing, you must manually include the fee rate in your **signed order payload**.

#### [​](https://docs.polymarket.com/developers/market-makers/maker-rebates-program\#step-1-fetch-the-fee-rate)  Step 1: Fetch the Fee Rate

Query the fee rate for the token ID before creating your order:

Copy

```
GET https://clob.polymarket.com/fee-rate?token_id={token_id}
```

**Response:**

Copy

```
{
  "fee_rate_bps": 1000
}
```

- **Fee-enabled markets** return a value like `1000`
- **Fee-free markets** return `0`

#### [​](https://docs.polymarket.com/developers/market-makers/maker-rebates-program\#step-2-include-in-your-signed-order)  Step 2: Include in Your Signed Order

Add the `feeRateBps` field to your order object. This value is **part of the signed payload**, the CLOB validates your signature against it.

Copy

```
{
  "salt": "12345",
  "maker": "0x...",
  "signer": "0x...",
  "taker": "0x...",
  "tokenId": "71321045679252212594626385532706912750332728571942532289631379312455583992563",
  "makerAmount": "50000000",
  "takerAmount": "100000000",
  "expiration": "0",
  "nonce": "0",
  "feeRateBps": "1000",
  "side": "0",
  "signatureType": 2,
  "signature": "0x..."
}
```

#### [​](https://docs.polymarket.com/developers/market-makers/maker-rebates-program\#step-3-sign-and-submit)  Step 3: Sign and Submit

1. Include `feeRateBps` in the order object **before signing**
2. Sign the complete order
3. POST to `/order` endpoint

**Important:** Always fetch `fee_rate_bps` dynamically, do not hardcode. The fee rate may vary by market or change over time. You only need to pass `feeRateBps`

See the [Create Order documentation](https://docs.polymarket.com/developers/CLOB/orders/create-order) for full signing details.

* * *

## [​](https://docs.polymarket.com/developers/market-makers/maker-rebates-program\#fee-behavior)  Fee Behavior

Fees are calculated in USDC and vary based on the share price. The effective rate **peaks at 50%** probability and decreases symmetrically toward the extremes.

### [​](https://docs.polymarket.com/developers/market-makers/maker-rebates-program\#fee-table-100-shares)  Fee Table (100 shares)

| Price | Trade Value | Fee (USDC) | Effective Rate |
| --- | --- | --- | --- |
| $0.10 | $10 | $0.02 | 0.20% |
| $0.20 | $20 | $0.13 | 0.64% |
| $0.30 | $30 | $0.33 | 1.10% |
| $0.40 | $40 | $0.58 | 1.44% |
| $0.50 | $50 | $0.78 | **1.56%** |
| $0.60 | $60 | $0.86 | 1.44% |
| $0.70 | $70 | $0.77 | 1.10% |
| $0.80 | $80 | $0.51 | 0.64% |
| $0.90 | $90 | $0.18 | 0.20% |

The maximum effective fee rate is **1.56%** at 50% probability. Fees are the same for both buying and selling.

* * *

## [​](https://docs.polymarket.com/developers/market-makers/maker-rebates-program\#maker-rebates)  Maker Rebates

### [​](https://docs.polymarket.com/developers/market-makers/maker-rebates-program\#how-rebates-work)  How Rebates Work

- **Eligibility:** Your orders must add liquidity (maker orders) and get filled
- **Calculation:** Proportional to your share of executed maker volume in each eligible market
- **Payment:** Daily in USDC, paid directly to your wallet

### [​](https://docs.polymarket.com/developers/market-makers/maker-rebates-program\#rebate-pool)  Rebate Pool

The rebate pool for each market is funded by taker fees collected in that market. The payout percentage is subject to change:

| Period | Maker Rebate | Distribution Method |
| --- | --- | --- |
| Jan 9 – Jan 11, 2026 (Until Sunday Midnight UTC) | 100% | Volume-weighted |
| Jan 12 – Jan 18, 2026 | 20% | Volume-weighted |
| Jan 19, 2026 – | 20% | Fee-curve weighted |

The rebate percentage is at the sole discretion of Polymarket and may change over time.

* * *

## [​](https://docs.polymarket.com/developers/market-makers/maker-rebates-program\#which-markets-have-fees)  Which Markets Have Fees?

Currently, only **15-minute crypto markets** have fees enabled. Query the fee-rate endpoint to check:

Copy

```
GET https://clob.polymarket.com/fee-rate?token_id={token_id}

# Fee-enabled: { "fee_rate_bps": 1000 }
# Fee-free:    { "fee_rate_bps": 0 }
```

* * *

## [​](https://docs.polymarket.com/developers/market-makers/maker-rebates-program\#related-documentation)  Related Documentation

[**Maker Rebates Program** \\
\\
User-facing overview with full fee tables](https://docs.polymarket.com/polymarket-learn/trading/maker-rebates-program) [**Create CLOB Order via REST API** \\
\\
Full order structure and signing documentation](https://docs.polymarket.com/developers/CLOB/orders/create-order)

[Liquidity Rewards](https://docs.polymarket.com/developers/market-makers/liquidity-rewards) [Data Feeds](https://docs.polymarket.com/developers/market-makers/data-feeds)

Ctrl+I

Assistant

Responses are generated using AI and may contain mistakes.