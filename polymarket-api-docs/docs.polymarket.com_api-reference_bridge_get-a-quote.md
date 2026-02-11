---
url: "https://docs.polymarket.com/api-reference/bridge/get-a-quote"
title: "Get a quote - Polymarket Documentation"
---

[Skip to main content](https://docs.polymarket.com/api-reference/bridge/get-a-quote#content-area)

[Polymarket Documentation home page![light logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-black.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=aff81820f1f3d577fecb3956a8a3bee1)![dark logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-white.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=3bc6857b5dbe8b74b9a7d40975c19b2b)](https://docs.polymarket.com/)

Search...

Ctrl K

Search...

Navigation

Bridge

Get a quote

[User Guide](https://docs.polymarket.com/polymarket-learn/get-started/what-is-polymarket) [For Developers](https://docs.polymarket.com/quickstart/overview) [Changelog](https://docs.polymarket.com/changelog/changelog)

Get a quote

cURL

Copy

```
curl --request POST \
  --url https://bridge.polymarket.com/quote \
  --header 'Content-Type: application/json' \
  --data '
{
  "fromAmountBaseUnit": "10000000",
  "fromChainId": "137",
  "fromTokenAddress": "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359",
  "recipientAddress": "0x17eC161f126e82A8ba337f4022d574DBEaFef575",
  "toChainId": "137",
  "toTokenAddress": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
}
'
```

200

Example

Copy

```
{
  "estCheckoutTimeMs": 25000,
  "estFeeBreakdown": {
    "appFeeLabel": "Fun.xyz fee",
    "appFeePercent": 0,
    "appFeeUsd": 0,
    "fillCostPercent": 0,
    "fillCostUsd": 0,
    "gasUsd": 0.003854,
    "maxSlippage": 0,
    "minReceived": 14.488305,
    "swapImpact": 0,
    "swapImpactUsd": 0,
    "totalImpact": 0,
    "totalImpactUsd": 0
  },
  "estInputUsd": 14.488305,
  "estOutputUsd": 14.488305,
  "estToTokenBaseUnit": "14491203",
  "quoteId": "0x00c34ba467184b0146406d62b0e60aaa24ed52460bd456222b6155a0d9de0ad5"
}
```

POST

/

quote

Try it

Get a quote

cURL

Copy

```
curl --request POST \
  --url https://bridge.polymarket.com/quote \
  --header 'Content-Type: application/json' \
  --data '
{
  "fromAmountBaseUnit": "10000000",
  "fromChainId": "137",
  "fromTokenAddress": "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359",
  "recipientAddress": "0x17eC161f126e82A8ba337f4022d574DBEaFef575",
  "toChainId": "137",
  "toTokenAddress": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
}
'
```

200

Example

Copy

```
{
  "estCheckoutTimeMs": 25000,
  "estFeeBreakdown": {
    "appFeeLabel": "Fun.xyz fee",
    "appFeePercent": 0,
    "appFeeUsd": 0,
    "fillCostPercent": 0,
    "fillCostUsd": 0,
    "gasUsd": 0.003854,
    "maxSlippage": 0,
    "minReceived": 14.488305,
    "swapImpact": 0,
    "swapImpactUsd": 0,
    "totalImpact": 0,
    "totalImpactUsd": 0
  },
  "estInputUsd": 14.488305,
  "estOutputUsd": 14.488305,
  "estToTokenBaseUnit": "14491203",
  "quoteId": "0x00c34ba467184b0146406d62b0e60aaa24ed52460bd456222b6155a0d9de0ad5"
}
```

#### Body

application/json

[​](https://docs.polymarket.com/api-reference/bridge/get-a-quote#body-from-amount-base-unit)

fromAmountBaseUnit

string

required

Amount of tokens to send

Example:

`"10000000"`

[​](https://docs.polymarket.com/api-reference/bridge/get-a-quote#body-from-chain-id)

fromChainId

string

required

Source Chain ID

Example:

`"137"`

[​](https://docs.polymarket.com/api-reference/bridge/get-a-quote#body-from-token-address)

fromTokenAddress

string

required

Source token address

Example:

`"0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359"`

[​](https://docs.polymarket.com/api-reference/bridge/get-a-quote#body-recipient-address)

recipientAddress

string

required

Address of the recipient

Example:

`"0x17eC161f126e82A8ba337f4022d574DBEaFef575"`

[​](https://docs.polymarket.com/api-reference/bridge/get-a-quote#body-to-chain-id)

toChainId

string

required

Destination Chain ID

Example:

`"137"`

[​](https://docs.polymarket.com/api-reference/bridge/get-a-quote#body-to-token-address)

toTokenAddress

string

required

Destination token address

Example:

`"0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"`

#### Response

200

application/json

Quote retrieved successfully

[​](https://docs.polymarket.com/api-reference/bridge/get-a-quote#response-est-checkout-time-ms)

estCheckoutTimeMs

integer

Estimated time to complete the checkout in milliseconds

Example:

`25000`

[​](https://docs.polymarket.com/api-reference/bridge/get-a-quote#response-est-fee-breakdown)

estFeeBreakdown

object

Breakdown of the estimated fees

Showchild attributes

[​](https://docs.polymarket.com/api-reference/bridge/get-a-quote#response-est-input-usd)

estInputUsd

number

Estimated token amount received in USD

Example:

`14.488305`

[​](https://docs.polymarket.com/api-reference/bridge/get-a-quote#response-est-output-usd)

estOutputUsd

number

Estimated token amount sent in USD

Example:

`14.488305`

[​](https://docs.polymarket.com/api-reference/bridge/get-a-quote#response-est-to-token-base-unit)

estToTokenBaseUnit

string

Estimated token amount received

Example:

`"14491203"`

[​](https://docs.polymarket.com/api-reference/bridge/get-a-quote#response-quote-id)

quoteId

string

Unique quote id of the request

Example:

`"0x00c34ba467184b0146406d62b0e60aaa24ed52460bd456222b6155a0d9de0ad5"`

[Get supported assets](https://docs.polymarket.com/api-reference/bridge/get-supported-assets) [Create deposit addresses](https://docs.polymarket.com/api-reference/bridge/create-deposit-addresses)

Ctrl+I

Assistant

Responses are generated using AI and may contain mistakes.