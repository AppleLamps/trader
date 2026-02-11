---
url: "https://docs.polymarket.com/developers/market-makers/introduction"
title: "Market Maker Introduction - Polymarket Documentation"
---

[Skip to main content](https://docs.polymarket.com/developers/market-makers/introduction#content-area)

[Polymarket Documentation home page![light logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-black.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=aff81820f1f3d577fecb3956a8a3bee1)![dark logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-white.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=3bc6857b5dbe8b74b9a7d40975c19b2b)](https://docs.polymarket.com/)

Search...

Ctrl K

Search...

Navigation

Market Makers

Market Maker Introduction

[User Guide](https://docs.polymarket.com/polymarket-learn/get-started/what-is-polymarket) [For Developers](https://docs.polymarket.com/quickstart/overview) [Changelog](https://docs.polymarket.com/changelog/changelog)

On this page

- [What is a Market Maker?](https://docs.polymarket.com/developers/market-makers/introduction#what-is-a-market-maker)
- [Getting Started](https://docs.polymarket.com/developers/market-makers/introduction#getting-started)
- [Available Tools](https://docs.polymarket.com/developers/market-makers/introduction#available-tools)
- [By Action Type](https://docs.polymarket.com/developers/market-makers/introduction#by-action-type)
- [Quick Reference](https://docs.polymarket.com/developers/market-makers/introduction#quick-reference)
- [Support](https://docs.polymarket.com/developers/market-makers/introduction#support)

## [​](https://docs.polymarket.com/developers/market-makers/introduction\#what-is-a-market-maker)  What is a Market Maker?

A Market Maker (MM) on Polymarket is a sophisticated trader who provides liquidity to prediction markets by continuously posting bid and ask orders. By “laying the spread,” market makers enable other users to trade efficiently while earning the spread as compensation for the risk they take.Market makers are essential to Polymarket’s ecosystem:

- **Provide liquidity** across all markets
- **Tighten spreads** for better user experience
- **Enable price discovery** through continuous quoting
- **Absorb trading flow** from retail and institutional users

**Not a Market Maker?** If you’re building an application that routes orders for your
users, see the [Builders Program](https://docs.polymarket.com/developers/builders/builder-intro) instead. Builders
get access to gasless transactions via the Relayer Client.

## [​](https://docs.polymarket.com/developers/market-makers/introduction\#getting-started)  Getting Started

To become a market maker on Polymarket:

1. **Complete setup** \- Deploy wallets, fund with USDCe, set token approvals
2. **Connect to data feeds** \- WebSocket for orderbook, RTDS for low-latency data
3. **Start quoting** \- Post orders via CLOB REST API

## [​](https://docs.polymarket.com/developers/market-makers/introduction\#available-tools)  Available Tools

### [​](https://docs.polymarket.com/developers/market-makers/introduction\#by-action-type)  By Action Type

[**Setup** \\
\\
Deposits, token approvals, wallet deployment, API keys](https://docs.polymarket.com/developers/market-makers/setup) [**Trading** \\
\\
CLOB order entry, order types, quoting best practices](https://docs.polymarket.com/developers/market-makers/trading) [**Data Feeds** \\
\\
WebSocket, RTDS, Gamma API, on-chain data](https://docs.polymarket.com/developers/market-makers/data-feeds) [**Inventory Management** \\
\\
Split, merge, and redeem outcome tokens](https://docs.polymarket.com/developers/market-makers/inventory) [**Liquidity Rewards** \\
\\
Earn rewards for providing liquidity](https://docs.polymarket.com/developers/market-makers/liquidity-rewards) [**Maker Rebates Program** \\
\\
Earn rebates for providing liquidity](https://docs.polymarket.com/developers/market-makers/maker-rebates-program)

## [​](https://docs.polymarket.com/developers/market-makers/introduction\#quick-reference)  Quick Reference

| Action | Tool | Documentation |
| --- | --- | --- |
| Deposit USDCe | Bridge API | [Bridge Overview](https://docs.polymarket.com/developers/misc-endpoints/bridge-overview) |
| Approve tokens | Relayer Client | [Setup Guide](https://docs.polymarket.com/developers/market-makers/setup) |
| Post limit orders | CLOB REST API | [CLOB Client](https://docs.polymarket.com/developers/CLOB/clients/methods-l2) |
| Monitor orderbook | WebSocket | [WebSocket Overview](https://docs.polymarket.com/developers/CLOB/websocket/wss-overview) |
| Low-latency data | RTDS | [Data Feeds](https://docs.polymarket.com/developers/market-makers/data-feeds) |
| Split USDCe to tokens | CTF / Relayer | [Inventory](https://docs.polymarket.com/developers/market-makers/inventory) |
| Merge tokens to USDCe | CTF / Relayer | [Inventory](https://docs.polymarket.com/developers/market-makers/inventory) |

## [​](https://docs.polymarket.com/developers/market-makers/introduction\#support)  Support

For market maker onboarding and support, contact [support@polymarket.com](mailto:support@polymarket.com).

[Endpoints](https://docs.polymarket.com/quickstart/reference/endpoints) [Setup](https://docs.polymarket.com/developers/market-makers/setup)

Ctrl+I

Assistant

Responses are generated using AI and may contain mistakes.