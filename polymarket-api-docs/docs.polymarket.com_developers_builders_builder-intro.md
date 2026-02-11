---
url: "https://docs.polymarket.com/developers/builders/builder-intro"
title: "Builder Program Introduction - Polymarket Documentation"
---

[Skip to main content](https://docs.polymarket.com/developers/builders/builder-intro#content-area)

[Polymarket Documentation home page![light logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-black.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=aff81820f1f3d577fecb3956a8a3bee1)![dark logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-white.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=3bc6857b5dbe8b74b9a7d40975c19b2b)](https://docs.polymarket.com/)

Search...

Ctrl K

Search...

Navigation

Polymarket Builders Program

Builder Program Introduction

[User Guide](https://docs.polymarket.com/polymarket-learn/get-started/what-is-polymarket) [For Developers](https://docs.polymarket.com/quickstart/overview) [Changelog](https://docs.polymarket.com/changelog/changelog)

On this page

- [What is a Builder?](https://docs.polymarket.com/developers/builders/builder-intro#what-is-a-builder)
- [Program Benefits](https://docs.polymarket.com/developers/builders/builder-intro#program-benefits)
- [Relayer Access](https://docs.polymarket.com/developers/builders/builder-intro#relayer-access)
- [Trading Attribution](https://docs.polymarket.com/developers/builders/builder-intro#trading-attribution)
- [Getting Started](https://docs.polymarket.com/developers/builders/builder-intro#getting-started)
- [SDKs & Libraries](https://docs.polymarket.com/developers/builders/builder-intro#sdks-%26-libraries)

## [​](https://docs.polymarket.com/developers/builders/builder-intro\#what-is-a-builder)  What is a Builder?

A “builder” is a person, group, or organization that routes orders from their users to Polymarket.
If you’ve created a platform that allows users to trade on Polymarket via your system, this program is for you.

* * *

## [​](https://docs.polymarket.com/developers/builders/builder-intro\#program-benefits)  Program Benefits

## Relayer Access

All onchain operations are gasless through our relayer

## Order Attribution

Get credited for orders and compete for weekly rewards on the Builder Leaderboard

## Fee Share

Earn a share of fees on routed orders

### [​](https://docs.polymarket.com/developers/builders/builder-intro\#relayer-access)  Relayer Access

We expose our relayer to builders, providing gasless transactions for users with
Polymarket’s Proxy Wallets deployed via [Relayer Client](https://docs.polymarket.com/developers/builders/relayer-client).When transactions are routed through proxy wallets, Polymarket pays all gas fees for:

- Deploying Gnosis Safe Wallets or Custom Proxy (Magic Link users) Wallets
- Token approvals (USDC, outcome tokens)
- CTF operations (split, merge, redeem)
- Order execution (via [CLOB API](https://docs.polymarket.com/developers/CLOB/introduction))

EOA wallets do not have relayer access. Users trading directly from an EOA pay their own gas fees.

### [​](https://docs.polymarket.com/developers/builders/builder-intro\#trading-attribution)  Trading Attribution

Attach custom headers to orders to identify your builder account:

- Orders attributed to your builder account
- Compete on the [Builder Leaderboard](https://builders.polymarket.com/) for weekly rewards
- Track performance via the Data API
  - [Leaderboard API](https://docs.polymarket.com/api-reference/builders/get-aggregated-builder-leaderboard): Get aggregated builder rankings for a time period
  - [Volume API](https://docs.polymarket.com/api-reference/builders/get-daily-builder-volume-time-series): Get daily time-series volume data for trend analysis

* * *

## [​](https://docs.polymarket.com/developers/builders/builder-intro\#getting-started)  Getting Started

1. **Get Builder Credentials**: Generate API keys from your [Builder Profile](https://docs.polymarket.com/developers/builders/builder-profile)
2. **Configure Order Attribution**: Set up CLOB client to credit trades to your account ( [guide](https://docs.polymarket.com/developers/builders/order-attribution))
3. **Enable Gasless Transactions**: Use the Relayer for gas-free wallet deployment and trading ( [guide](https://docs.polymarket.com/developers/builders/relayer-client))

See [Example Apps](https://docs.polymarket.com/developers/builders/examples) for complete Next.js reference implementations.

* * *

## [​](https://docs.polymarket.com/developers/builders/builder-intro\#sdks-&-libraries)  SDKs & Libraries

[**CLOB Client (TypeScript)** \\
\\
Place orders with builder attribution](https://github.com/Polymarket/clob-client) [**CLOB Client (Python)** \\
\\
Place orders with builder attribution](https://github.com/Polymarket/py-clob-client) [**CLOB Client (Rust)** \\
\\
Place orders with builder attribution](https://github.com/Polymarket/rs-clob-client) [**Relayer Client (TypeScript)** \\
\\
Gasless onchain transactions for your users](https://github.com/Polymarket/builder-relayer-client) [**Relayer Client (Python)** \\
\\
Gasless onchain transactions for your users](https://github.com/Polymarket/py-builder-relayer-client) [**Signing SDK (TypeScript)** \\
\\
Sign builder authentication headers](https://github.com/Polymarket/builder-signing-sdk) [**Signing SDK (Python)** \\
\\
Sign builder authentication headers](https://github.com/Polymarket/py-builder-signing-sdk)

[Inventory Management](https://docs.polymarket.com/developers/market-makers/inventory) [Builder Tiers](https://docs.polymarket.com/developers/builders/builder-tiers)

Ctrl+I

Assistant

Responses are generated using AI and may contain mistakes.