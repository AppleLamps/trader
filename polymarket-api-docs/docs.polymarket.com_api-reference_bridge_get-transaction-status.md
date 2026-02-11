---
url: "https://docs.polymarket.com/api-reference/bridge/get-transaction-status"
title: "Get transaction status - Polymarket Documentation"
---

[Skip to main content](https://docs.polymarket.com/api-reference/bridge/get-transaction-status#content-area)

[Polymarket Documentation home page![light logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-black.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=aff81820f1f3d577fecb3956a8a3bee1)![dark logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-white.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=3bc6857b5dbe8b74b9a7d40975c19b2b)](https://docs.polymarket.com/)

Search...

Ctrl K

Search...

Navigation

Bridge

Get transaction status

[User Guide](https://docs.polymarket.com/polymarket-learn/get-started/what-is-polymarket) [For Developers](https://docs.polymarket.com/quickstart/overview) [Changelog](https://docs.polymarket.com/changelog/changelog)

Get transaction status

cURL

Copy

```
curl --request GET \
  --url https://bridge.polymarket.com/status/{address}
```

200

400

500

Copy

```
{
  "transactions": [\
    {\
      "fromChainId": "1151111081099710",\
      "fromTokenAddress": "11111111111111111111111111111111",\
      "fromAmountBaseUnit": "13566635",\
      "toChainId": "137",\
      "toTokenAddress": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",\
      "status": "DEPOSIT_DETECTED"\
    },\
    {\
      "fromChainId": "1151111081099710",\
      "fromTokenAddress": "11111111111111111111111111111111",\
      "fromAmountBaseUnit": "13400000",\
      "toChainId": "137",\
      "toTokenAddress": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",\
      "createdTimeMs": 1757646914535,\
      "status": "PROCESSING"\
    },\
    {\
      "fromChainId": "1151111081099710",\
      "fromTokenAddress": "11111111111111111111111111111111",\
      "fromAmountBaseUnit": "13500152",\
      "toChainId": "137",\
      "toTokenAddress": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",\
      "txHash": "3atr19NAiNCYt24RHM1WnzZp47RXskpTDzspJoCBBaMFwUB8fk37hFkxz35P5UEnnmWz21rb2t5wJ8pq3EE2XnxU",\
      "createdTimeMs": 1757531217339,\
      "status": "COMPLETED"\
    }\
  ]
}
```

GET

/

status

/

{address}

Try it

Get transaction status

cURL

Copy

```
curl --request GET \
  --url https://bridge.polymarket.com/status/{address}
```

200

400

500

Copy

```
{
  "transactions": [\
    {\
      "fromChainId": "1151111081099710",\
      "fromTokenAddress": "11111111111111111111111111111111",\
      "fromAmountBaseUnit": "13566635",\
      "toChainId": "137",\
      "toTokenAddress": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",\
      "status": "DEPOSIT_DETECTED"\
    },\
    {\
      "fromChainId": "1151111081099710",\
      "fromTokenAddress": "11111111111111111111111111111111",\
      "fromAmountBaseUnit": "13400000",\
      "toChainId": "137",\
      "toTokenAddress": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",\
      "createdTimeMs": 1757646914535,\
      "status": "PROCESSING"\
    },\
    {\
      "fromChainId": "1151111081099710",\
      "fromTokenAddress": "11111111111111111111111111111111",\
      "fromAmountBaseUnit": "13500152",\
      "toChainId": "137",\
      "toTokenAddress": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",\
      "txHash": "3atr19NAiNCYt24RHM1WnzZp47RXskpTDzspJoCBBaMFwUB8fk37hFkxz35P5UEnnmWz21rb2t5wJ8pq3EE2XnxU",\
      "createdTimeMs": 1757531217339,\
      "status": "COMPLETED"\
    }\
  ]
}
```

#### Path Parameters

[​](https://docs.polymarket.com/api-reference/bridge/get-transaction-status#parameter-address)

address

string

required

The address to query for transaction status (EVM, SVM, or BTC address from the `/deposit` or `/withdraw` response)

#### Response

200

application/json

Successfully retrieved transaction status

[​](https://docs.polymarket.com/api-reference/bridge/get-transaction-status#response-transactions)

transactions

object\[\]

List of transactions for the given address

Showchild attributes

[Create withdrawal addresses](https://docs.polymarket.com/api-reference/bridge/create-withdrawal-addresses) [Overview](https://docs.polymarket.com/developers/subgraph/overview)

Ctrl+I

Assistant

Responses are generated using AI and may contain mistakes.