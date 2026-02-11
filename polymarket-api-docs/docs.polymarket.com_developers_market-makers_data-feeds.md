---
url: "https://docs.polymarket.com/developers/market-makers/data-feeds"
title: "Data Feeds - Polymarket Documentation"
---

[Skip to main content](https://docs.polymarket.com/developers/market-makers/data-feeds#content-area)

[Polymarket Documentation home page![light logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-black.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=aff81820f1f3d577fecb3956a8a3bee1)![dark logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-white.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=3bc6857b5dbe8b74b9a7d40975c19b2b)](https://docs.polymarket.com/)

Search...

Ctrl K

Search...

Navigation

Market Makers

Data Feeds

[User Guide](https://docs.polymarket.com/polymarket-learn/get-started/what-is-polymarket) [For Developers](https://docs.polymarket.com/quickstart/overview) [Changelog](https://docs.polymarket.com/changelog/changelog)

On this page

- [Overview](https://docs.polymarket.com/developers/market-makers/data-feeds#overview)
- [WebSocket Feeds](https://docs.polymarket.com/developers/market-makers/data-feeds#websocket-feeds)
- [Connecting](https://docs.polymarket.com/developers/market-makers/data-feeds#connecting)
- [Available Channels](https://docs.polymarket.com/developers/market-makers/data-feeds#available-channels)
- [User Channel (Authenticated)](https://docs.polymarket.com/developers/market-makers/data-feeds#user-channel-authenticated)
- [Best Practices](https://docs.polymarket.com/developers/market-makers/data-feeds#best-practices)
- [Gamma API](https://docs.polymarket.com/developers/market-makers/data-feeds#gamma-api)
- [Get Markets](https://docs.polymarket.com/developers/market-makers/data-feeds#get-markets)
- [Get Events](https://docs.polymarket.com/developers/market-makers/data-feeds#get-events)
- [Key Fields for MMs](https://docs.polymarket.com/developers/market-makers/data-feeds#key-fields-for-mms)
- [Onchain Data](https://docs.polymarket.com/developers/market-makers/data-feeds#onchain-data)
- [Data Sources](https://docs.polymarket.com/developers/market-makers/data-feeds#data-sources)
- [RPC Providers](https://docs.polymarket.com/developers/market-makers/data-feeds#rpc-providers)
- [UMA Oracle](https://docs.polymarket.com/developers/market-makers/data-feeds#uma-oracle)
- [Related Documentation](https://docs.polymarket.com/developers/market-makers/data-feeds#related-documentation)

## [​](https://docs.polymarket.com/developers/market-makers/data-feeds\#overview)  Overview

Market makers need fast, reliable data to price markets and manage inventory. Polymarket provides several data feeds at different latency and detail levels.

| Feed | Latency | Use Case | Access |
| --- | --- | --- | --- |
| WebSocket | ~100ms | Standard MM operations | Public |
| Gamma API | ~1s | Market metadata, indexing | Public |
| Onchain | Block time | Settlement, resolution | Public |

## [​](https://docs.polymarket.com/developers/market-makers/data-feeds\#websocket-feeds)  WebSocket Feeds

The WebSocket API provides real-time market data with low latency. This is sufficient for most market making strategies.

### [​](https://docs.polymarket.com/developers/market-makers/data-feeds\#connecting)  Connecting

Copy

```
const ws = new WebSocket("wss://ws-subscriptions-clob.polymarket.com/ws/market");

ws.onopen = () => {
  // Subscribe to orderbook updates
  ws.send(JSON.stringify({
    type: "market",
    assets_ids: [tokenId]
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  // Handle orderbook update
};
```

### [​](https://docs.polymarket.com/developers/market-makers/data-feeds\#available-channels)  Available Channels

| Channel | Message Types | Documentation |
| --- | --- | --- |
| `market` | `book`, `price_change`, `last_trade_price` | [Market Channel](https://docs.polymarket.com/developers/CLOB/websocket/market-channel) |
| `user` | Order fills, cancellations | [User Channel](https://docs.polymarket.com/developers/CLOB/websocket/user-channel) |

### [​](https://docs.polymarket.com/developers/market-makers/data-feeds\#user-channel-authenticated)  User Channel (Authenticated)

Monitor your order activity in real-time:

Copy

```
// Requires authentication
const userWs = new WebSocket("wss://ws-subscriptions-clob.polymarket.com/ws/user");

userWs.onopen = () => {
  userWs.send(JSON.stringify({
    type: "user",
    auth: {
      apiKey: "your-api-key",
      secret: "your-secret",
      passphrase: "your-passphrase"
    },
    markets: [conditionId] // Optional: filter to specific markets
  }));
};

userWs.onmessage = (event) => {
  const data = JSON.parse(event.data);
  // Handle order fills, cancellations, etc.
};
```

See [WebSocket Authentication](https://docs.polymarket.com/developers/CLOB/websocket/wss-auth) for auth details.

### [​](https://docs.polymarket.com/developers/market-makers/data-feeds\#best-practices)  Best Practices

1. **Reconnection logic** \- Implement automatic reconnection with exponential backoff
2. **Heartbeats** \- Respond to ping messages to maintain connection
3. **Local orderbook** \- Maintain a local copy and apply incremental updates
4. **Sequence numbers** \- Track sequence to detect missed messages

See [WebSocket Overview](https://docs.polymarket.com/developers/CLOB/websocket/wss-overview) for complete documentation.

## [​](https://docs.polymarket.com/developers/market-makers/data-feeds\#gamma-api)  Gamma API

The Gamma API provides market metadata and indexing. Use it for:

- Market titles, slugs, categories
- Event/condition mapping
- Volume and liquidity data
- Outcome token metadata

### [​](https://docs.polymarket.com/developers/market-makers/data-feeds\#get-markets)  Get Markets

Copy

```
const response = await fetch(
  "https://gamma-api.polymarket.com/markets?active=true"
);
const markets = await response.json();
```

### [​](https://docs.polymarket.com/developers/market-makers/data-feeds\#get-events)  Get Events

Copy

```
const response = await fetch(
  "https://gamma-api.polymarket.com/events?slug=us-presidential-election"
);
const event = await response.json();
```

### [​](https://docs.polymarket.com/developers/market-makers/data-feeds\#key-fields-for-mms)  Key Fields for MMs

| Field | Description |
| --- | --- |
| `conditionId` | Unique market identifier |
| `clobTokenIds` | Outcome token IDs |
| `outcomes` | Outcome names |
| `outcomePrices` | Current outcome prices |
| `volume` | Trading volume |
| `liquidity` | Current liquidity |

See [Gamma API Overview](https://docs.polymarket.com/developers/gamma-markets-api/overview) for complete documentation.

## [​](https://docs.polymarket.com/developers/market-makers/data-feeds\#onchain-data)  Onchain Data

For settlement, resolution, and position tracking, market makers may query onchain data directly.

### [​](https://docs.polymarket.com/developers/market-makers/data-feeds\#data-sources)  Data Sources

| Data | Source | Use Case |
| --- | --- | --- |
| Token balances | ERC1155 `balanceOf` | Position tracking |
| Resolution | UMA Oracle events | Pre-resolution risk modeling |
| Condition resolution | CTF contract | Post-resolution redemption |

### [​](https://docs.polymarket.com/developers/market-makers/data-feeds\#rpc-providers)  RPC Providers

Common providers for Polygon:

- Alchemy
- QuickNode
- Infura

### [​](https://docs.polymarket.com/developers/market-makers/data-feeds\#uma-oracle)  UMA Oracle

Markets are resolved via UMA’s Optimistic Oracle. Monitor resolution events for risk management.See [Resolution](https://docs.polymarket.com/developers/resolution/UMA) for details on the resolution process.

## [​](https://docs.polymarket.com/developers/market-makers/data-feeds\#related-documentation)  Related Documentation

[**WebSocket Overview** \\
\\
Complete WebSocket documentation](https://docs.polymarket.com/developers/CLOB/websocket/wss-overview) [**Gamma API** \\
\\
Market metadata and indexing](https://docs.polymarket.com/developers/gamma-markets-api/overview) [**Resolution** \\
\\
UMA Oracle resolution process](https://docs.polymarket.com/developers/resolution/UMA)

[Maker Rebates Program](https://docs.polymarket.com/developers/market-makers/maker-rebates-program) [Inventory Management](https://docs.polymarket.com/developers/market-makers/inventory)

Ctrl+I

Assistant

Responses are generated using AI and may contain mistakes.