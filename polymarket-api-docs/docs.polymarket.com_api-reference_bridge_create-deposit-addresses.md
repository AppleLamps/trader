---
url: "https://docs.polymarket.com/api-reference/bridge/create-deposit-addresses"
title: "Create deposit addresses - Polymarket Documentation"
---

[Skip to main content](https://docs.polymarket.com/api-reference/bridge/create-deposit-addresses#content-area)

[Polymarket Documentation home page![light logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-black.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=aff81820f1f3d577fecb3956a8a3bee1)![dark logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-white.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=3bc6857b5dbe8b74b9a7d40975c19b2b)](https://docs.polymarket.com/)

Search...

Ctrl K

Search...

Navigation

Bridge

Create deposit addresses

[User Guide](https://docs.polymarket.com/polymarket-learn/get-started/what-is-polymarket) [For Developers](https://docs.polymarket.com/quickstart/overview) [Changelog](https://docs.polymarket.com/changelog/changelog)

Create deposit addresses

cURL

Copy

```
curl --request POST \
  --url https://bridge.polymarket.com/deposit \
  --header 'Content-Type: application/json' \
  --data '
{
  "address": "0x56687bf447db6ffa42ffe2204a05edaa20f55839"
}
'
```

201

400

500

Copy

```
{
  "address": {
    "evm": "0x23566f8b2E82aDfCf01846E54899d110e97AC053",
    "svm": "CrvTBvzryYxBHbWu2TiQpcqD5M7Le7iBKzVmEj3f36Jb",
    "btc": "bc1q8eau83qffxcj8ht4hsjdza3lha9r3egfqysj3g"
  },
  "note": "Only certain chains and tokens are supported. See /supported-assets for details."
}
```

POST

/

deposit

Try it

Create deposit addresses

cURL

Copy

```
curl --request POST \
  --url https://bridge.polymarket.com/deposit \
  --header 'Content-Type: application/json' \
  --data '
{
  "address": "0x56687bf447db6ffa42ffe2204a05edaa20f55839"
}
'
```

201

400

500

Copy

```
{
  "address": {
    "evm": "0x23566f8b2E82aDfCf01846E54899d110e97AC053",
    "svm": "CrvTBvzryYxBHbWu2TiQpcqD5M7Le7iBKzVmEj3f36Jb",
    "btc": "bc1q8eau83qffxcj8ht4hsjdza3lha9r3egfqysj3g"
  },
  "note": "Only certain chains and tokens are supported. See /supported-assets for details."
}
```

#### Body

application/json

[​](https://docs.polymarket.com/api-reference/bridge/create-deposit-addresses#body-address)

address

string

required

Your Polymarket wallet address where deposited funds will be credited as USDC.e

Example:

`"0x56687bf447db6ffa42ffe2204a05edaa20f55839"`

#### Response

201

application/json

Deposit addresses created successfully

[​](https://docs.polymarket.com/api-reference/bridge/create-deposit-addresses#response-address)

address

object

Deposit addresses for different blockchain networks

Showchild attributes

[​](https://docs.polymarket.com/api-reference/bridge/create-deposit-addresses#response-note)

note

string

Additional information about the deposit addresses

Example:

`"Only certain chains and tokens are supported. See /supported-assets for details."`

[Get a quote](https://docs.polymarket.com/api-reference/bridge/get-a-quote) [Create withdrawal addresses](https://docs.polymarket.com/api-reference/bridge/create-withdrawal-addresses)

Ctrl+I

Assistant

Responses are generated using AI and may contain mistakes.