---
url: "https://docs.polymarket.com/developers/builders/examples"
title: "Examples - Polymarket Documentation"
---

[Skip to main content](https://docs.polymarket.com/developers/builders/examples#content-area)

[Polymarket Documentation home page![light logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-black.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=aff81820f1f3d577fecb3956a8a3bee1)![dark logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-white.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=3bc6857b5dbe8b74b9a7d40975c19b2b)](https://docs.polymarket.com/)

Search...

Ctrl K

Search...

Navigation

Polymarket Builders Program

Examples

[User Guide](https://docs.polymarket.com/polymarket-learn/get-started/what-is-polymarket) [For Developers](https://docs.polymarket.com/quickstart/overview) [Changelog](https://docs.polymarket.com/changelog/changelog)

On this page

- [Overview](https://docs.polymarket.com/developers/builders/examples#overview)
- [Safe Wallet Examples](https://docs.polymarket.com/developers/builders/examples#safe-wallet-examples)
- [Proxy Wallet Examples](https://docs.polymarket.com/developers/builders/examples#proxy-wallet-examples)
- [What Each Demo Covers](https://docs.polymarket.com/developers/builders/examples#what-each-demo-covers)

## [​](https://docs.polymarket.com/developers/builders/examples\#overview)  Overview

These open-source demo applications show how to integrate Polymarket’s CLOB Client and Builder Relayer Client for gasless trading with builder order attribution.

## Authentication

Multiple wallet providers

## Gasless Trading

Safe & Proxy wallet support

## Full Integration

Orders, positions, CTF ops

* * *

## [​](https://docs.polymarket.com/developers/builders/examples\#safe-wallet-examples)  Safe Wallet Examples

Deploy Gnosis Safe wallets for your users:

[**wagmi + Safe** \\
\\
MetaMask, Phantom, Rabby, and other browser wallets](https://github.com/Polymarket/wagmi-safe-builder-example) [**Privy + Safe** \\
\\
Privy embedded wallets](https://github.com/Polymarket/privy-safe-builder-example) [**Magic Link + Safe** \\
\\
Magic Link email/social authentication](https://github.com/Polymarket/magic-safe-builder-example) [**Turnkey + Safe** \\
\\
Turnkey embedded wallets](https://github.com/Polymarket/turnkey-safe-builder-example)

## [​](https://docs.polymarket.com/developers/builders/examples\#proxy-wallet-examples)  Proxy Wallet Examples

For existing Magic Link users from Polymarket.com:

[**Magic Link + Proxy** \\
\\
Auto-deploying proxy wallets for Polymarket.com Magic users](https://github.com/Polymarket/magic-proxy-builder-example)

* * *

## [​](https://docs.polymarket.com/developers/builders/examples\#what-each-demo-covers)  What Each Demo Covers

- Authentication

- Wallet Operations

- Trading


- User sign-in via wallet provider
- User API credential derivation (L2 auth)
- Builder config with remote signing
- Signature types for Safe vs Proxy wallets

- Safe wallet deployment via Relayer
- Batch token approvals (USDC.e + outcome tokens)
- CTF operations (split, merge, redeem)
- Transaction monitoring

- CLOB client initialization
- Order placement with builder attribution
- Position and order management
- Market discovery via Gamma API

[Relayer Client](https://docs.polymarket.com/developers/builders/relayer-client) [Blockchain Data Resources](https://docs.polymarket.com/developers/builders/blockchain-data-resources)

Ctrl+I

Assistant

Responses are generated using AI and may contain mistakes.