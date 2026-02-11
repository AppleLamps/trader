---
url: "https://docs.polymarket.com/developers/misc-endpoints/bridge-overview"
title: "Overview - Polymarket Documentation"
---

[Skip to main content](https://docs.polymarket.com/developers/misc-endpoints/bridge-overview#content-area)

[Polymarket Documentation home page![light logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-black.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=aff81820f1f3d577fecb3956a8a3bee1)![dark logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-white.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=3bc6857b5dbe8b74b9a7d40975c19b2b)](https://docs.polymarket.com/)

Search...

Ctrl K

Search...

Navigation

Bridge & Swap

Overview

[User Guide](https://docs.polymarket.com/polymarket-learn/get-started/what-is-polymarket) [For Developers](https://docs.polymarket.com/quickstart/overview) [Changelog](https://docs.polymarket.com/changelog/changelog)

On this page

- [USDC.e on Polygon](https://docs.polymarket.com/developers/misc-endpoints/bridge-overview#usdc-e-on-polygon)
- [Base URL](https://docs.polymarket.com/developers/misc-endpoints/bridge-overview#base-url)
- [Key Features](https://docs.polymarket.com/developers/misc-endpoints/bridge-overview#key-features)
- [Endpoints](https://docs.polymarket.com/developers/misc-endpoints/bridge-overview#endpoints)

The Polymarket Bridge API enables seamless deposits and withdrawals between multiple networks and Polymarket.

### [​](https://docs.polymarket.com/developers/misc-endpoints/bridge-overview\#usdc-e-on-polygon)  USDC.e on Polygon

**Polymarket uses USDC.e (Bridged USDC) on Polygon as collateral** for all trading activities. USDC.e is the bridged version of USDC from Ethereum, and it serves as the native currency for placing orders and settling trades on Polymarket.When you deposit assets to Polymarket:

1. You can deposit from various supported chains (Ethereum, Solana, Arbitrum, Base, etc.)
2. Your assets are automatically bridged/swapped to USDC.e on Polygon
3. USDC.e is credited to your Polymarket wallet so you can trade on any market

## [​](https://docs.polymarket.com/developers/misc-endpoints/bridge-overview\#base-url)  Base URL

Copy

```
https://bridge.polymarket.com
```

## [​](https://docs.polymarket.com/developers/misc-endpoints/bridge-overview\#key-features)  Key Features

- **Multi-chain deposits**: Bridge assets from EVM chains (Ethereum, Arbitrum, Base, etc.), Solana, and Bitcoin
- **Multi-chain withdrawals**: Withdraw USDC.e to any supported chain and token
- **Automatic conversion**: Assets are automatically bridged and swapped
- **Simple addressing**: One deposit address per blockchain type (EVM, SVM, BTC)

## [​](https://docs.polymarket.com/developers/misc-endpoints/bridge-overview\#endpoints)  Endpoints

- `GET /supported-assets` \- Get all supported chains and tokens
- `POST /quote` \- Get a quote for a deposit or withdrawal
- `POST /deposit` \- Create deposit addresses for bridging assets to Polymarket
- `POST /withdraw` \- Create withdrawal addresses for bridging assets from Polymarket
- `GET /status/{address}` \- Get transaction status for a given address

[Get daily builder volume time-series](https://docs.polymarket.com/api-reference/builders/get-daily-builder-volume-time-series) [Get supported assets](https://docs.polymarket.com/api-reference/bridge/get-supported-assets)

Ctrl+I

Assistant

Responses are generated using AI and may contain mistakes.