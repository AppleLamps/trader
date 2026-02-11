---
url: "https://docs.polymarket.com/quickstart/introduction/rate-limits"
title: "API Rate Limits - Polymarket Documentation"
---

[Skip to main content](https://docs.polymarket.com/quickstart/introduction/rate-limits#content-area)

[Polymarket Documentation home page![light logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-black.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=aff81820f1f3d577fecb3956a8a3bee1)![dark logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-white.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=3bc6857b5dbe8b74b9a7d40975c19b2b)](https://docs.polymarket.com/)

Search...

Ctrl K

Search...

Navigation

Developer Quickstart

API Rate Limits

[User Guide](https://docs.polymarket.com/polymarket-learn/get-started/what-is-polymarket) [For Developers](https://docs.polymarket.com/quickstart/overview) [Changelog](https://docs.polymarket.com/changelog/changelog)

On this page

- [How Rate Limiting Works](https://docs.polymarket.com/quickstart/introduction/rate-limits#how-rate-limiting-works)
- [General Rate Limits](https://docs.polymarket.com/quickstart/introduction/rate-limits#general-rate-limits)
- [Data API Rate Limits](https://docs.polymarket.com/quickstart/introduction/rate-limits#data-api-rate-limits)
- [GAMMA API Rate Limits](https://docs.polymarket.com/quickstart/introduction/rate-limits#gamma-api-rate-limits)
- [CLOB API Rate Limits](https://docs.polymarket.com/quickstart/introduction/rate-limits#clob-api-rate-limits)
- [General CLOB Endpoints](https://docs.polymarket.com/quickstart/introduction/rate-limits#general-clob-endpoints)
- [CLOB Market Data](https://docs.polymarket.com/quickstart/introduction/rate-limits#clob-market-data)
- [CLOB Ledger Endpoints](https://docs.polymarket.com/quickstart/introduction/rate-limits#clob-ledger-endpoints)
- [CLOB Markets & Pricing](https://docs.polymarket.com/quickstart/introduction/rate-limits#clob-markets-%26-pricing)
- [CLOB Authentication](https://docs.polymarket.com/quickstart/introduction/rate-limits#clob-authentication)
- [CLOB Trading Endpoints](https://docs.polymarket.com/quickstart/introduction/rate-limits#clob-trading-endpoints)
- [Other API Rate Limits](https://docs.polymarket.com/quickstart/introduction/rate-limits#other-api-rate-limits)

## [​](https://docs.polymarket.com/quickstart/introduction/rate-limits\#how-rate-limiting-works)  How Rate Limiting Works

All rate limits are enforced using Cloudflare’s throttling system. When you exceed the maximum configured rate for any endpoint, requests are throttled rather than immediately rejected. This means:

- **Throttling**: Requests over the limit are delayed/queued rather than dropped
- **Burst Allowances**: Some endpoints allow short bursts above the sustained rate
- **Time Windows**: Limits reset based on sliding time windows (e.g., per 10 seconds, per minute)

## [​](https://docs.polymarket.com/quickstart/introduction/rate-limits\#general-rate-limits)  General Rate Limits

| Endpoint | Limit | Notes |
| --- | --- | --- |
| General Rate Limiting | 15000 requests / 10s | Throttle requests over the maximum configured rate |
| ”OK” Endpoint | 100 requests / 10s | Throttle requests over the maximum configured rate |

## [​](https://docs.polymarket.com/quickstart/introduction/rate-limits\#data-api-rate-limits)  Data API Rate Limits

| Endpoint | Limit | Notes |
| --- | --- | --- |
| Data API (General) | 1000 requests / 10s | Throttle requests over the maximum configured rate |
| Data API `/trades` | 200 requests / 10s | Throttle requests over the maximum configured rate |
| Data API `/positions` | 150 requests / 10s | Throttle requests over the maximum configured rate |
| Data API `/closed-positions` | 150 requests / 10s | Throttle requests over the maximum configured rate |
| Data API “OK” Endpoint | 100 requests / 10s | Throttle requests over the maximum configured rate |

## [​](https://docs.polymarket.com/quickstart/introduction/rate-limits\#gamma-api-rate-limits)  GAMMA API Rate Limits

| Endpoint | Limit | Notes |
| --- | --- | --- |
| GAMMA (General) | 4000 requests / 10s | Throttle requests over the maximum configured rate |
| GAMMA Get Comments | 200 requests / 10s | Throttle requests over the maximum configured rate |
| GAMMA `/events` | 500 requests / 10s | Throttle requests over the maximum configured rate |
| GAMMA `/markets` | 300 requests / 10s | Throttle requests over the maximum configured rate |
| GAMMA `/markets` /events listing | 900 requests / 10s | Throttle requests over the maximum configured rate |
| GAMMA Tags | 200 requests / 10s | Throttle requests over the maximum configured rate |
| GAMMA Search | 350 requests / 10s | Throttle requests over the maximum configured rate |

## [​](https://docs.polymarket.com/quickstart/introduction/rate-limits\#clob-api-rate-limits)  CLOB API Rate Limits

### [​](https://docs.polymarket.com/quickstart/introduction/rate-limits\#general-clob-endpoints)  General CLOB Endpoints

| Endpoint | Limit | Notes |
| --- | --- | --- |
| CLOB (General) | 9000 requests / 10s | Throttle requests over the maximum configured rate |
| CLOB GET Balance Allowance | 200 requests / 10s | Throttle requests over the maximum configured rate |
| CLOB UPDATE Balance Allowance | 50 requests / 10s | Throttle requests over the maximum configured rate |

### [​](https://docs.polymarket.com/quickstart/introduction/rate-limits\#clob-market-data)  CLOB Market Data

| Endpoint | Limit | Notes |
| --- | --- | --- |
| CLOB `/book` | 1500 requests / 10s | Throttle requests over the maximum configured rate |
| CLOB `/books` | 500 requests / 10s | Throttle requests over the maximum configured rate |
| CLOB `/price` | 1500 requests / 10s | Throttle requests over the maximum configured rate |
| CLOB `/prices` | 500 requests / 10s | Throttle requests over the maximum configured rate |
| CLOB `/midprice` | 1500 requests / 10s | Throttle requests over the maximum configured rate |
| CLOB `/midprices` | 500 requests / 10s | Throttle requests over the maximum configured rate |

### [​](https://docs.polymarket.com/quickstart/introduction/rate-limits\#clob-ledger-endpoints)  CLOB Ledger Endpoints

| Endpoint | Limit | Notes |
| --- | --- | --- |
| CLOB Ledger (`/trades``/orders``/notifications``/order`) | 900 requests / 10s | Throttle requests over the maximum configured rate |
| CLOB Ledger `/data/orders` | 500 requests / 10s | Throttle requests over the maximum configured rate |
| CLOB Ledger `/data/trades` | 500 requests / 10s | Throttle requests over the maximum configured rate |
| CLOB `/notifications` | 125 requests / 10s | Throttle requests over the maximum configured rate |

### [​](https://docs.polymarket.com/quickstart/introduction/rate-limits\#clob-markets-&-pricing)  CLOB Markets & Pricing

| Endpoint | Limit | Notes |
| --- | --- | --- |
| CLOB Price History | 1000 requests / 10s | Throttle requests over the maximum configured rate |
| CLOB Market Tick Size | 200 requests / 10s | Throttle requests over the maximum configured rate |

### [​](https://docs.polymarket.com/quickstart/introduction/rate-limits\#clob-authentication)  CLOB Authentication

| Endpoint | Limit | Notes |
| --- | --- | --- |
| CLOB API Keys | 100 requests / 10s | Throttle requests over the maximum configured rate |

### [​](https://docs.polymarket.com/quickstart/introduction/rate-limits\#clob-trading-endpoints)  CLOB Trading Endpoints

| Endpoint | Limit | Notes |
| --- | --- | --- |
| CLOB POST `/order` | 3500 requests / 10s (500/s) | BURST - Throttle requests over the maximum configured rate |
| CLOB POST `/order` | 36000 requests / 10 minutes (60/s) | Throttle requests over the maximum configured rate |
| CLOB DELETE `/order` | 3000 requests / 10s (300/s) | BURST - Throttle requests over the maximum configured rate |
| CLOB DELETE `/order` | 30000 requests / 10 minutes (50/s) | Throttle requests over the maximum configured rate |
| CLOB POST `/orders` | 1000 requests / 10s (100/s) | BURST - Throttle requests over the maximum configured rate |
| CLOB POST `/orders` | 15000 requests / 10 minutes (25/s) | Throttle requests over the maximum configured rate |
| CLOB DELETE `/orders` | 1000 requests / 10s (100/s) | BURST - Throttle requests over the maximum configured rate |
| CLOB DELETE `/orders` | 15000 requests / 10 minutes (25/s) | Throttle requests over the maximum configured rate |
| CLOB DELETE `/cancel-all` | 250 requests / 10s (25/s) | BURST - Throttle requests over the maximum configured rate |
| CLOB DELETE `/cancel-all` | 6000 requests / 10 minutes (10/s) | Throttle requests over the maximum configured rate |
| CLOB DELETE `/cancel-market-orders` | 1000 requests / 10s (100/s) | BURST - Throttle requests over the maximum configured rate |
| CLOB DELETE `/cancel-market-orders` | 1500 requests / 10 minutes (25/s) | Throttle requests over the maximum configured rate |

## [​](https://docs.polymarket.com/quickstart/introduction/rate-limits\#other-api-rate-limits)  Other API Rate Limits

| Endpoint | Limit | Notes |
| --- | --- | --- |
| RELAYER `/submit` | 25 requests / 1 minute | Throttle requests over the maximum configured rate |
| User PNL API | 200 requests / 10s | Throttle requests over the maximum configured rate |

[Glossary](https://docs.polymarket.com/quickstart/reference/glossary) [Endpoints](https://docs.polymarket.com/quickstart/reference/endpoints)

Ctrl+I

Assistant

Responses are generated using AI and may contain mistakes.