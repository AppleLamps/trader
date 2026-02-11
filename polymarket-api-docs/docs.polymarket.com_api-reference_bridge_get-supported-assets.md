---
url: "https://docs.polymarket.com/api-reference/bridge/get-supported-assets"
title: "Get supported assets - Polymarket Documentation"
---

[Skip to main content](https://docs.polymarket.com/api-reference/bridge/get-supported-assets#content-area)

[Polymarket Documentation home page![light logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-black.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=aff81820f1f3d577fecb3956a8a3bee1)![dark logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-white.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=3bc6857b5dbe8b74b9a7d40975c19b2b)](https://docs.polymarket.com/)

Search...

Ctrl K

Search...

Navigation

Bridge

Get supported assets

[User Guide](https://docs.polymarket.com/polymarket-learn/get-started/what-is-polymarket) [For Developers](https://docs.polymarket.com/quickstart/overview) [Changelog](https://docs.polymarket.com/changelog/changelog)

Get supported assets

cURL

Copy

```
curl --request GET \
  --url https://bridge.polymarket.com/supported-assets
```

200

500

Copy

```
{
  "supportedAssets": [\
    {\
      "chainId": "1",\
      "chainName": "Ethereum",\
      "token": {\
        "name": "USD Coin",\
        "symbol": "USDC",\
        "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",\
        "decimals": 6\
      },\
      "minCheckoutUsd": 45\
    }\
  ]
}
```

GET

/

supported-assets

Try it

Get supported assets

cURL

Copy

```
curl --request GET \
  --url https://bridge.polymarket.com/supported-assets
```

200

500

Copy

```
{
  "supportedAssets": [\
    {\
      "chainId": "1",\
      "chainName": "Ethereum",\
      "token": {\
        "name": "USD Coin",\
        "symbol": "USDC",\
        "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",\
        "decimals": 6\
      },\
      "minCheckoutUsd": 45\
    }\
  ]
}
```

#### Response

200

application/json

Successfully retrieved supported assets

[​](https://docs.polymarket.com/api-reference/bridge/get-supported-assets#response-supported-assets)

supportedAssets

object\[\]

List of supported assets with minimum amounts for deposits and withdrawals

Showchild attributes

[Overview](https://docs.polymarket.com/developers/misc-endpoints/bridge-overview) [Get a quote](https://docs.polymarket.com/api-reference/bridge/get-a-quote)

Ctrl+I

Assistant

Responses are generated using AI and may contain mistakes.