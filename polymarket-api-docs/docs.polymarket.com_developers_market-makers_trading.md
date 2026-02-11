---
url: "https://docs.polymarket.com/developers/market-makers/trading"
title: "Trading - Polymarket Documentation"
---

[Skip to main content](https://docs.polymarket.com/developers/market-makers/trading#content-area)

[Polymarket Documentation home page![light logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-black.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=aff81820f1f3d577fecb3956a8a3bee1)![dark logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-white.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=3bc6857b5dbe8b74b9a7d40975c19b2b)](https://docs.polymarket.com/)

Search...

Ctrl K

Search...

Navigation

Market Makers

Trading

[User Guide](https://docs.polymarket.com/polymarket-learn/get-started/what-is-polymarket) [For Developers](https://docs.polymarket.com/quickstart/overview) [Changelog](https://docs.polymarket.com/changelog/changelog)

On this page

- [Overview](https://docs.polymarket.com/developers/market-makers/trading#overview)
- [Order Entry](https://docs.polymarket.com/developers/market-makers/trading#order-entry)
- [Posting Limit Orders](https://docs.polymarket.com/developers/market-makers/trading#posting-limit-orders)
- [Batch Orders](https://docs.polymarket.com/developers/market-makers/trading#batch-orders)
- [Order Types](https://docs.polymarket.com/developers/market-makers/trading#order-types)
- [When to Use Each](https://docs.polymarket.com/developers/market-makers/trading#when-to-use-each)
- [Order Management](https://docs.polymarket.com/developers/market-makers/trading#order-management)
- [Cancel Orders](https://docs.polymarket.com/developers/market-makers/trading#cancel-orders)
- [Get Active Orders](https://docs.polymarket.com/developers/market-makers/trading#get-active-orders)
- [Best Practices](https://docs.polymarket.com/developers/market-makers/trading#best-practices)
- [Quote Management](https://docs.polymarket.com/developers/market-makers/trading#quote-management)
- [Latency Optimization](https://docs.polymarket.com/developers/market-makers/trading#latency-optimization)
- [Risk Management](https://docs.polymarket.com/developers/market-makers/trading#risk-management)
- [Tick Sizes](https://docs.polymarket.com/developers/market-makers/trading#tick-sizes)
- [Fee Structure](https://docs.polymarket.com/developers/market-makers/trading#fee-structure)
- [Related Documentation](https://docs.polymarket.com/developers/market-makers/trading#related-documentation)

## [​](https://docs.polymarket.com/developers/market-makers/trading\#overview)  Overview

Market makers primarily interact with Polymarket through the CLOB (Central Limit Order Book) API to post and manage limit orders.

## [​](https://docs.polymarket.com/developers/market-makers/trading\#order-entry)  Order Entry

### [​](https://docs.polymarket.com/developers/market-makers/trading\#posting-limit-orders)  Posting Limit Orders

Use the CLOB client to create and post limit orders:

Copy

```
import { ClobClient, Side, OrderType } from "@polymarket/clob-client";

const client = new ClobClient(
  "https://clob.polymarket.com",
  137,
  wallet,
  credentials,
  signatureType,
  funder
);

// Post a bid (buy order)
const bidOrder = await client.createAndPostOrder({
  tokenID: "34097058504275310827233323421517291090691602969494795225921954353603704046623",
  side: Side.BUY,
  price: 0.48,
  size: 1000,
  orderType: OrderType.GTC
});

// Post an ask (sell order)
const askOrder = await client.createAndPostOrder({
  tokenID: "34097058504275310827233323421517291090691602969494795225921954353603704046623",
  side: Side.SELL,
  price: 0.52,
  size: 1000,
  orderType: OrderType.GTC
});
```

See [Create Order](https://docs.polymarket.com/developers/CLOB/clients/methods-l1#createandpostorder) for full documentation.

### [​](https://docs.polymarket.com/developers/market-makers/trading\#batch-orders)  Batch Orders

For efficiency, post multiple orders in a single request:

Copy

```
const orders = await Promise.all([\
  client.createOrder({ tokenID, side: Side.BUY, price: 0.48, size: 500 }),\
  client.createOrder({ tokenID, side: Side.BUY, price: 0.47, size: 500 }),\
  client.createOrder({ tokenID, side: Side.SELL, price: 0.52, size: 500 }),\
  client.createOrder({ tokenID, side: Side.SELL, price: 0.53, size: 500 })\
]);

const response = await client.postOrders(
  orders.map(order => ({ order, orderType: OrderType.GTC }))
);
```

See [Post Orders Batch](https://docs.polymarket.com/developers/CLOB/clients/methods-l2#postorders) for details.

## [​](https://docs.polymarket.com/developers/market-makers/trading\#order-types)  Order Types

| Type | Behavior | MM Use Case |
| --- | --- | --- |
| **GTC** (Good Till Cancelled) | Rests on book until filled or cancelled | Default for passive quoting |
| **GTD** (Good Till Date) | Auto-expires at specified time | Auto-expire before events |
| **FOK** (Fill or Kill) | Fill entirely immediately or cancel | Aggressive rebalancing (all or nothing) |
| **FAK** (Fill and Kill) | Fill available immediately, cancel rest | Partial rebalancing acceptable |

### [​](https://docs.polymarket.com/developers/market-makers/trading\#when-to-use-each)  When to Use Each

**For passive market making (maker orders):**

- **GTC** \- Standard quotes that sit on the book
- **GTD** \- Time-limited quotes (e.g., expire before market close)

**For rebalancing (taker orders):**

- **FOK** \- When you need exact size or nothing
- **FAK** \- When partial fills are acceptable

Copy

```
// GTD example: expire in 1 hour
const expiringOrder = await client.createOrder({
  tokenID,
  side: Side.BUY,
  price: 0.50,
  size: 1000,
  orderType: OrderType.GTD,
  expiration: Math.floor(Date.now() / 1000) + 3600 // 1 hour from now
});
```

## [​](https://docs.polymarket.com/developers/market-makers/trading\#order-management)  Order Management

### [​](https://docs.polymarket.com/developers/market-makers/trading\#cancel-orders)  Cancel Orders

Cancel individual orders or all orders:

Copy

```
// Cancel single order
await client.cancelOrder(orderId);

// Cancel multiple orders in a single calls
await client.cancelOrders(orderIds: string[]);

// Cancel all orders for a market
await client.cancelMarketOrders(conditionId);

// Cancel all orders
await client.cancelAll();
```

See [Cancel Orders](https://docs.polymarket.com/developers/CLOB/clients/methods-l2#cancelorder) for full documentation.

### [​](https://docs.polymarket.com/developers/market-makers/trading\#get-active-orders)  Get Active Orders

Monitor your open orders:

Copy

```
// Get active order
const order = await client.getOrder(orderId);

// Get active orders optionally filtered
const orders = await client.getOpenOrders({
  id?: string; // Order ID (hash)
  market?: string; // Market condition ID
  asset_id?: string; // Token ID
});
```

See [Get Active Orders](https://docs.polymarket.com/developers/CLOB/clients/methods-l2#getorder) for details.

## [​](https://docs.polymarket.com/developers/market-makers/trading\#best-practices)  Best Practices

### [​](https://docs.polymarket.com/developers/market-makers/trading\#quote-management)  Quote Management

1. **Two-sided quoting** \- Post both bids and asks to earn maximum [liquidity rewards](https://docs.polymarket.com/developers/market-makers/liquidity-rewards)
2. **Monitor inventory** \- Skew quotes based on your position
3. **Cancel stale quotes** \- Remove orders when market conditions change
4. **Use GTD for events** \- Auto-expire quotes before known events

### [​](https://docs.polymarket.com/developers/market-makers/trading\#latency-optimization)  Latency Optimization

1. **Batch orders** \- Use `postOrders()` instead of multiple `createAndPostOrder()` calls
2. **WebSocket for data** \- Use WebSocket feeds instead of polling REST endpoints

### [​](https://docs.polymarket.com/developers/market-makers/trading\#risk-management)  Risk Management

1. **Size limits** \- Check token balances before quoting; don’t exceed inventory
2. **Price guards** \- Validate against book midpoint; reject outlier prices
3. **Kill switch** \- Use `cancelAll()` on error or position breach
4. **Monitor fills** \- Subscribe to WebSocket user channel for real-time fill updates

## [​](https://docs.polymarket.com/developers/market-makers/trading\#tick-sizes)  Tick Sizes

Markets have different minimum price increments:

Copy

```
const tickSize = await client.getTickSize(tokenID);
// Returns: "0.1" | "0.01" | "0.001" | "0.0001"
```

Ensure your prices conform to the market’s tick size.

## [​](https://docs.polymarket.com/developers/market-makers/trading\#fee-structure)  Fee Structure

| Role | Fee |
| --- | --- |
| Maker | 0 bps |
| Taker | 0 bps |

Current fees are 0% for both makers and takers. See [CLOB Introduction](https://docs.polymarket.com/developers/CLOB/introduction) for fee calculation details.

## [​](https://docs.polymarket.com/developers/market-makers/trading\#related-documentation)  Related Documentation

[**CLOB Client Overview** \\
\\
Complete client method reference](https://docs.polymarket.com/developers/CLOB/clients/methods-overview) [**L2 Methods** \\
\\
Authenticated order management methods](https://docs.polymarket.com/developers/CLOB/clients/methods-l2) [**WebSocket Feeds** \\
\\
Real-time order and market data](https://docs.polymarket.com/developers/CLOB/websocket/wss-overview) [**Liquidity Rewards** \\
\\
Earn rewards for providing liquidity](https://docs.polymarket.com/developers/market-makers/liquidity-rewards)

[Setup](https://docs.polymarket.com/developers/market-makers/setup) [Liquidity Rewards](https://docs.polymarket.com/developers/market-makers/liquidity-rewards)

Ctrl+I

Assistant

Responses are generated using AI and may contain mistakes.