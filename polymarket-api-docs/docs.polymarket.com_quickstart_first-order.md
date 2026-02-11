---
url: "https://docs.polymarket.com/quickstart/first-order"
title: "Placing Your First Order - Polymarket Documentation"
---

[Skip to main content](https://docs.polymarket.com/quickstart/first-order#content-area)

[Polymarket Documentation home page![light logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-black.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=aff81820f1f3d577fecb3956a8a3bee1)![dark logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-white.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=3bc6857b5dbe8b74b9a7d40975c19b2b)](https://docs.polymarket.com/)

Search...

Ctrl K

Search...

Navigation

Developer Quickstart

Placing Your First Order

[User Guide](https://docs.polymarket.com/polymarket-learn/get-started/what-is-polymarket) [For Developers](https://docs.polymarket.com/quickstart/overview) [Changelog](https://docs.polymarket.com/changelog/changelog)

On this page

- [Installation](https://docs.polymarket.com/quickstart/first-order#installation)
- [Step 1: Initialize Client with Private Key](https://docs.polymarket.com/quickstart/first-order#step-1-initialize-client-with-private-key)
- [Step 2: Derive User API Credentials](https://docs.polymarket.com/quickstart/first-order#step-2-derive-user-api-credentials)
- [Step 3: Configure Signature Type and Funder](https://docs.polymarket.com/quickstart/first-order#step-3-configure-signature-type-and-funder)
- [Step 4: Reinitialize with Full Authentication](https://docs.polymarket.com/quickstart/first-order#step-4-reinitialize-with-full-authentication)
- [Step 5: Place an Order](https://docs.polymarket.com/quickstart/first-order#step-5-place-an-order)
- [Step 6: Check Your Orders](https://docs.polymarket.com/quickstart/first-order#step-6-check-your-orders)
- [Troubleshooting](https://docs.polymarket.com/quickstart/first-order#troubleshooting)
- [Adding Builder API Credentials](https://docs.polymarket.com/quickstart/first-order#adding-builder-api-credentials)

This guide walks you through placing an order on Polymarket using your own wallet.

* * *

## [​](https://docs.polymarket.com/quickstart/first-order\#installation)  Installation

TypeScript

Python

Rust

Copy

```
npm install @polymarket/clob-client ethers@5
```

* * *

## [​](https://docs.polymarket.com/quickstart/first-order\#step-1-initialize-client-with-private-key)  Step 1: Initialize Client with Private Key

TypeScript

Python

Copy

```
import { ClobClient } from "@polymarket/clob-client";
import { Wallet } from "ethers"; // v5.8.0

const HOST = "https://clob.polymarket.com";
const CHAIN_ID = 137; // Polygon mainnet
const signer = new Wallet(process.env.PRIVATE_KEY);

const client = new ClobClient(HOST, CHAIN_ID, signer);
```

* * *

## [​](https://docs.polymarket.com/quickstart/first-order\#step-2-derive-user-api-credentials)  Step 2: Derive User API Credentials

Your private key is used once to derive API credentials. These credentials authenticate all subsequent requests.

TypeScript

Python

Copy

```
// Get existing API key, or create one if none exists
const userApiCreds = await client.createOrDeriveApiKey();

console.log("API Key:", userApiCreds.apiKey);
console.log("Secret:", userApiCreds.secret);
console.log("Passphrase:", userApiCreds.passphrase);
```

* * *

## [​](https://docs.polymarket.com/quickstart/first-order\#step-3-configure-signature-type-and-funder)  Step 3: Configure Signature Type and Funder

Before reinitializing the client, determine your **signature type** and **funder address**:

| How do you want to trade? | Type | Value | Funder Address |
| --- | --- | --- | --- |
| I want to use an EOA wallet. It holds USDCe and position tokens, and I’ll pay my own gas. | EOA | `0` | Your EOA wallet address |
| I want to trade through my Polymarket.com account (Magic Link email/Google login). | POLY\_PROXY | `1` | Your proxy wallet address |
| I want to trade through my Polymarket.com account (browser wallet connection). | GNOSIS\_SAFE | `2` | Your proxy wallet address |

If you have a Polymarket.com account, your funds are in a proxy wallet (visible in the profile dropdown). Use type 1 or 2. Type 0 is for standalone EOA wallets only.

* * *

## [​](https://docs.polymarket.com/quickstart/first-order\#step-4-reinitialize-with-full-authentication)  Step 4: Reinitialize with Full Authentication

TypeScript

Python

Copy

```
// Choose based on your wallet type (see table above)
const SIGNATURE_TYPE = 0; // EOA example
const FUNDER_ADDRESS = signer.address; // For EOA, funder is your wallet

const client = new ClobClient(
  HOST,
  CHAIN_ID,
  signer,
  userApiCreds,
  SIGNATURE_TYPE,
  FUNDER_ADDRESS
);
```

**Do not use Builder API credentials in place of User API credentials!** Builder credentials are for order attribution, not user authentication. See [Builder Order Attribution](https://docs.polymarket.com/developers/builders/order-attribution).

* * *

## [​](https://docs.polymarket.com/quickstart/first-order\#step-5-place-an-order)  Step 5: Place an Order

Now you’re ready to trade! First, get a token ID from the [Gamma API](https://docs.polymarket.com/developers/gamma-markets-api/get-markets).

TypeScript

Python

Copy

```
import { Side, OrderType } from "@polymarket/clob-client";

// Get market info first
const market = await client.getMarket("TOKEN_ID");

const response = await client.createAndPostOrder(
  {
    tokenID: "TOKEN_ID",
    price: 0.50,        // Price per share ($0.50)
    size: 10,           // Number of shares
    side: Side.BUY,     // BUY or SELL
  },
  {
    tickSize: market.tickSize,
    negRisk: market.negRisk,    // true for multi-outcome events
  },
  OrderType.GTC  // Good-Til-Cancelled
);

console.log("Order ID:", response.orderID);
console.log("Status:", response.status);
```

* * *

## [​](https://docs.polymarket.com/quickstart/first-order\#step-6-check-your-orders)  Step 6: Check Your Orders

TypeScript

Python

Copy

```
// View all open orders
const openOrders = await client.getOpenOrders();
console.log(`You have ${openOrders.length} open orders`);

// View your trade history
const trades = await client.getTrades();
console.log(`You've made ${trades.length} trades`);

// Cancel an order
await client.cancelOrder(response.orderID);
```

* * *

## [​](https://docs.polymarket.com/quickstart/first-order\#troubleshooting)  Troubleshooting

Invalid Signature / L2 Auth Not Available

Wrong private key, signature type, or funder address for the derived User API credentials.Double check the following values when creating User API credentials via `createOrDeriveApiKey()`:

- Do not use Builder API credentials in place of User API credentials
- Check `signatureType` matches your account type (0, 1, or 2)
- Ensure `funder` is correct for your wallet type

Unauthorized / Invalid API Key

Wrong API key, secret, or passphrase.Re-derive credentials with `createOrDeriveApiKey()` and update your config.

Not Enough Balance / Allowance

Either not enough USDCe / position tokens in your funder address, or you lack approvals to spend your tokens.

- Deposit USDCe to your funder address.
- Ensure you have more USDCe than what’s committed in open orders.
- Check that you’ve set all necessary token approvals.

Blocked by Cloudflare / Geoblock

You’re trying to place a trade from a restricted region.See [Geographic Restrictions](https://docs.polymarket.com/developers/CLOB/geoblock) for details.

* * *

## [​](https://docs.polymarket.com/quickstart/first-order\#adding-builder-api-credentials)  Adding Builder API Credentials

If you’re building an app that routes orders for your users, you can add builder credentials to get attribution on the [Builder Leaderboard](https://builders.polymarket.com/):

TypeScript

Copy

```
import { BuilderConfig, BuilderApiKeyCreds } from "@polymarket/builder-signing-sdk";

const builderCreds: BuilderApiKeyCreds = {
  key: process.env.POLY_BUILDER_API_KEY!,
  secret: process.env.POLY_BUILDER_SECRET!,
  passphrase: process.env.POLY_BUILDER_PASSPHRASE!,
};

const builderConfig = new BuilderConfig({ localBuilderCreds: builderCreds });

// Add builderConfig as the last parameter
const client = new ClobClient(
  HOST,
  CHAIN_ID,
  signer,
  userApiCreds,
  signatureType,
  funderAddress,
  undefined,
  false,
  builderConfig
);
```

Builder credentials are **separate** from user credentials. You use your builder
credentials to tag orders, but each user still needs their own L2 credentials to trade.

[**Full Builder Guide** \\
\\
Complete documentation for order attribution and gasless transactions](https://docs.polymarket.com/developers/builders/order-attribution)

[Fetching Market Data](https://docs.polymarket.com/quickstart/fetching-data) [Glossary](https://docs.polymarket.com/quickstart/reference/glossary)

Ctrl+I

Assistant

Responses are generated using AI and may contain mistakes.