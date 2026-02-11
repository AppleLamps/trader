---
url: "https://docs.polymarket.com/quickstart/reference/endpoints"
title: "Endpoints - Polymarket Documentation"
---

[Skip to main content](https://docs.polymarket.com/quickstart/reference/endpoints#content-area)

[Polymarket Documentation home page![light logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-black.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=aff81820f1f3d577fecb3956a8a3bee1)![dark logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-white.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=3bc6857b5dbe8b74b9a7d40975c19b2b)](https://docs.polymarket.com/)

Search...

Ctrl K

Search...

Navigation

Developer Quickstart

Endpoints

[User Guide](https://docs.polymarket.com/polymarket-learn/get-started/what-is-polymarket) [For Developers](https://docs.polymarket.com/quickstart/overview) [Changelog](https://docs.polymarket.com/changelog/changelog)

On this page

- [REST APIs](https://docs.polymarket.com/quickstart/reference/endpoints#rest-apis)
- [WebSocket Endpoints](https://docs.polymarket.com/quickstart/reference/endpoints#websocket-endpoints)
- [Quick Reference](https://docs.polymarket.com/quickstart/reference/endpoints#quick-reference)
- [CLOB API](https://docs.polymarket.com/quickstart/reference/endpoints#clob-api)
- [Gamma API](https://docs.polymarket.com/quickstart/reference/endpoints#gamma-api)
- [Data API](https://docs.polymarket.com/quickstart/reference/endpoints#data-api)
- [CLOB WebSocket](https://docs.polymarket.com/quickstart/reference/endpoints#clob-websocket)
- [RTDS (Real-Time Data Stream)](https://docs.polymarket.com/quickstart/reference/endpoints#rtds-real-time-data-stream)

All base URLs for Polymarket APIs. See individual API documentation for available routes and parameters.

* * *

## [​](https://docs.polymarket.com/quickstart/reference/endpoints\#rest-apis)  REST APIs

| API | Base URL | Description |
| --- | --- | --- |
| **CLOB API** | `https://clob.polymarket.com` | Order management, prices, orderbooks |
| **Gamma API** | `https://gamma-api.polymarket.com` | Market discovery, metadata, events |
| **Data API** | `https://data-api.polymarket.com` | User positions, activity, history |

* * *

## [​](https://docs.polymarket.com/quickstart/reference/endpoints\#websocket-endpoints)  WebSocket Endpoints

| Service | URL | Description |
| --- | --- | --- |
| **CLOB WebSocket** | `wss://ws-subscriptions-clob.polymarket.com/ws/` | Orderbook updates, order status |
| **RTDS** | `wss://ws-live-data.polymarket.com` | Low-latency crypto prices, comments |

* * *

## [​](https://docs.polymarket.com/quickstart/reference/endpoints\#quick-reference)  Quick Reference

### [​](https://docs.polymarket.com/quickstart/reference/endpoints\#clob-api)  CLOB API

Copy

```
https://clob.polymarket.com
```

Common endpoints:

- `GET /price` — Get current price for a token
- `GET /book` — Get orderbook for a token
- `GET /midpoint` — Get midpoint price
- `POST /order` — Place an order (auth required)
- `DELETE /order` — Cancel an order (auth required)

[Full CLOB documentation →](https://docs.polymarket.com/developers/CLOB/introduction)

### [​](https://docs.polymarket.com/quickstart/reference/endpoints\#gamma-api)  Gamma API

Copy

```
https://gamma-api.polymarket.com
```

Common endpoints:

- `GET /events` — List events
- `GET /markets` — List markets
- `GET /events/{id}` — Get event details

[Full Gamma documentation →](https://docs.polymarket.com/developers/gamma-markets-api/overview)

### [​](https://docs.polymarket.com/quickstart/reference/endpoints\#data-api)  Data API

Copy

```
https://data-api.polymarket.com
```

Common endpoints:

- `GET /positions` — Get user positions
- `GET /activity` — Get user activity
- `GET /trades` — Get trade history

[Full Data API documentation →](https://docs.polymarket.com/developers/misc-endpoints/data-api-get-positions)

### [​](https://docs.polymarket.com/quickstart/reference/endpoints\#clob-websocket)  CLOB WebSocket

Copy

```
wss://ws-subscriptions-clob.polymarket.com/ws/
```

Channels:

- `market` — Orderbook and price updates (public)
- `user` — Order status updates (authenticated)

[Full WebSocket documentation →](https://docs.polymarket.com/developers/CLOB/websocket/wss-overview)

### [​](https://docs.polymarket.com/quickstart/reference/endpoints\#rtds-real-time-data-stream)  RTDS (Real-Time Data Stream)

Copy

```
wss://ws-live-data.polymarket.com
```

Channels:

- Crypto price feeds
- Comment streams

[Full RTDS documentation →](https://docs.polymarket.com/developers/RTDS/RTDS-overview)

[API Rate Limits](https://docs.polymarket.com/quickstart/introduction/rate-limits) [Market Maker Introduction](https://docs.polymarket.com/developers/market-makers/introduction)

Ctrl+I

Assistant

Responses are generated using AI and may contain mistakes.