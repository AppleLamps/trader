---
url: "https://docs.polymarket.com/api-reference/bridge/create-withdrawal-addresses"
title: "Create withdrawal addresses - Polymarket Documentation"
---

[Skip to main content](https://docs.polymarket.com/api-reference/bridge/create-withdrawal-addresses#content-area)

[Polymarket Documentation home page![light logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-black.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=aff81820f1f3d577fecb3956a8a3bee1)![dark logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-white.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=3bc6857b5dbe8b74b9a7d40975c19b2b)](https://docs.polymarket.com/)

Search...

Ctrl K

Search...

Navigation

Bridge

Create withdrawal addresses

[User Guide](https://docs.polymarket.com/polymarket-learn/get-started/what-is-polymarket) [For Developers](https://docs.polymarket.com/quickstart/overview) [Changelog](https://docs.polymarket.com/changelog/changelog)

Create withdrawal addresses

cURL

Copy

```
curl --request POST \
  --url https://bridge.polymarket.com/withdraw \
  --header 'Content-Type: application/json' \
  --data '
{
  "address": "0x9156dd10bea4c8d7e2d591b633d1694b1d764756",
  "toChainId": "1",
  "toTokenAddress": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
  "recipientAddr": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
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
  "note": "Send funds to these addresses to bridge to your destination chain and token."
}
```

POST

/

withdraw

Try it

Create withdrawal addresses

cURL

Copy

```
curl --request POST \
  --url https://bridge.polymarket.com/withdraw \
  --header 'Content-Type: application/json' \
  --data '
{
  "address": "0x9156dd10bea4c8d7e2d591b633d1694b1d764756",
  "toChainId": "1",
  "toTokenAddress": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
  "recipientAddr": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
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
  "note": "Send funds to these addresses to bridge to your destination chain and token."
}
```

#### Body

application/json

[​](https://docs.polymarket.com/api-reference/bridge/create-withdrawal-addresses#body-address)

address

string

required

Source Polymarket wallet address on Polygon

Example:

`"0x56687bf447db6ffa42ffe2204a05edaa20f55839"`

[​](https://docs.polymarket.com/api-reference/bridge/create-withdrawal-addresses#body-to-chain-id)

toChainId

string

required

Destination chain ID (e.g., "1" for Ethereum, "8453" for Base, "1151111081099710" for Solana)

Example:

`"1"`

[​](https://docs.polymarket.com/api-reference/bridge/create-withdrawal-addresses#body-to-token-address)

toTokenAddress

string

required

Destination token contract address

Example:

`"0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"`

[​](https://docs.polymarket.com/api-reference/bridge/create-withdrawal-addresses#body-recipient-addr)

recipientAddr

string

required

Destination wallet address where funds will be sent

Example:

`"0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"`

#### Response

201

application/json

Withdrawal addresses created successfully

[​](https://docs.polymarket.com/api-reference/bridge/create-withdrawal-addresses#response-address)

address

object

Deposit addresses for different blockchain networks

Showchild attributes

[​](https://docs.polymarket.com/api-reference/bridge/create-withdrawal-addresses#response-note)

note

string

Additional information about the deposit addresses

Example:

`"Only certain chains and tokens are supported. See /supported-assets for details."`

[Create deposit addresses](https://docs.polymarket.com/api-reference/bridge/create-deposit-addresses) [Get transaction status](https://docs.polymarket.com/api-reference/bridge/get-transaction-status)

Ctrl+I

Assistant

Responses are generated using AI and may contain mistakes.