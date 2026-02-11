---
url: "https://docs.polymarket.com/developers/sports-websocket/overview"
title: "Overview - Polymarket Documentation"
---

[Skip to main content](https://docs.polymarket.com/developers/sports-websocket/overview#content-area)

[Polymarket Documentation home page![light logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-black.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=aff81820f1f3d577fecb3956a8a3bee1)![dark logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-white.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=3bc6857b5dbe8b74b9a7d40975c19b2b)](https://docs.polymarket.com/)

Search...

Ctrl K

Search...

Navigation

Sports Websocket

Overview

[User Guide](https://docs.polymarket.com/polymarket-learn/get-started/what-is-polymarket) [For Developers](https://docs.polymarket.com/quickstart/overview) [Changelog](https://docs.polymarket.com/changelog/changelog)

On this page

- [How It Works](https://docs.polymarket.com/developers/sports-websocket/overview#how-it-works)
- [Connection Management](https://docs.polymarket.com/developers/sports-websocket/overview#connection-management)
- [Automatic Ping/Pong Heartbeat](https://docs.polymarket.com/developers/sports-websocket/overview#automatic-ping%2Fpong-heartbeat)
- [Connection Health](https://docs.polymarket.com/developers/sports-websocket/overview#connection-health)
- [Session Affinity](https://docs.polymarket.com/developers/sports-websocket/overview#session-affinity)
- [Next Steps](https://docs.polymarket.com/developers/sports-websocket/overview#next-steps)

The Polymarket Sports WebSocket API provides real-time sports results updates. Clients connect to receive live match data including scores, periods, and game status as events happen.**Endpoint:**

Copy

```
wss://sports-api.polymarket.com/ws
```

No authentication is required. This is a public broadcast channel that streams updates for all active sports events.

## [​](https://docs.polymarket.com/developers/sports-websocket/overview\#how-it-works)  How It Works

Once connected, clients automatically receive JSON messages whenever a sports event updates. There is no subscription message required—simply connect and start receiving data.

* * *

## [​](https://docs.polymarket.com/developers/sports-websocket/overview\#connection-management)  Connection Management

### [​](https://docs.polymarket.com/developers/sports-websocket/overview\#automatic-ping/pong-heartbeat)  Automatic Ping/Pong Heartbeat

The server sends PING messages at regular intervals. Clients **must** respond with PONG to maintain the connection.

| Parameter | Default | Description |
| --- | --- | --- |
| PING Interval | 5 seconds | How often the server sends PING messages |
| PONG Timeout | 10 seconds | How long the server waits for a PONG response |

If your client doesn’t respond to PING within 10 seconds, the connection will be closed automatically.

### [​](https://docs.polymarket.com/developers/sports-websocket/overview\#connection-health)  Connection Health

- Server sends `PING` → Client must respond with `PONG`
- No response within timeout → Connection terminated
- Clients should implement automatic reconnection with exponential backoff

* * *

## [​](https://docs.polymarket.com/developers/sports-websocket/overview\#session-affinity)  Session Affinity

The server uses cookie-based session affinity (`sports-results` cookie) to ensure clients maintain connection to the same backend instance. This is handled automatically by the browser.

* * *

## [​](https://docs.polymarket.com/developers/sports-websocket/overview\#next-steps)  Next Steps

[**Message Format** \\
\\
Understand the structure of sports update messages](https://docs.polymarket.com/developers/sports-websocket/message-format) [**Quickstart** \\
\\
Implementation examples in JavaScript and TypeScript](https://docs.polymarket.com/developers/sports-websocket/quickstart)

[Market Channel](https://docs.polymarket.com/developers/CLOB/websocket/market-channel) [Message Format](https://docs.polymarket.com/developers/sports-websocket/message-format)

Ctrl+I

Assistant

Responses are generated using AI and may contain mistakes.