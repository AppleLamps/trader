---
url: "https://docs.polymarket.com/api-reference/builders/get-aggregated-builder-leaderboard"
title: "Get aggregated builder leaderboard - Polymarket Documentation"
---

[Skip to main content](https://docs.polymarket.com/api-reference/builders/get-aggregated-builder-leaderboard#content-area)

[Polymarket Documentation home page![light logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-black.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=aff81820f1f3d577fecb3956a8a3bee1)![dark logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-white.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=3bc6857b5dbe8b74b9a7d40975c19b2b)](https://docs.polymarket.com/)

Search...

Ctrl K

Search...

Navigation

Builders

Get aggregated builder leaderboard

[User Guide](https://docs.polymarket.com/polymarket-learn/get-started/what-is-polymarket) [For Developers](https://docs.polymarket.com/quickstart/overview) [Changelog](https://docs.polymarket.com/changelog/changelog)

Get aggregated builder leaderboard

cURL

Copy

```
curl --request GET \
  --url 'https://data-api.polymarket.com/v1/builders/leaderboard?timePeriod=DAY&limit=25'
```

200

400

500

Copy

```
[\
  {\
    "rank": "<string>",\
    "builder": "<string>",\
    "volume": 123,\
    "activeUsers": 123,\
    "verified": true,\
    "builderLogo": "<string>"\
  }\
]
```

GET

/

v1

/

builders

/

leaderboard

Try it

Get aggregated builder leaderboard

cURL

Copy

```
curl --request GET \
  --url 'https://data-api.polymarket.com/v1/builders/leaderboard?timePeriod=DAY&limit=25'
```

200

400

500

Copy

```
[\
  {\
    "rank": "<string>",\
    "builder": "<string>",\
    "volume": 123,\
    "activeUsers": 123,\
    "verified": true,\
    "builderLogo": "<string>"\
  }\
]
```

#### Query Parameters

[​](https://docs.polymarket.com/api-reference/builders/get-aggregated-builder-leaderboard#parameter-time-period)

timePeriod

enum<string>

default:DAY

The time period to aggregate results over.

Available options:

`DAY`,

`WEEK`,

`MONTH`,

`ALL`

[​](https://docs.polymarket.com/api-reference/builders/get-aggregated-builder-leaderboard#parameter-limit)

limit

integer

default:25

Maximum number of builders to return

Required range: `0 <= x <= 50`

[​](https://docs.polymarket.com/api-reference/builders/get-aggregated-builder-leaderboard#parameter-offset)

offset

integer

default:0

Starting index for pagination

Required range: `0 <= x <= 1000`

#### Response

200

application/json

Success

[​](https://docs.polymarket.com/api-reference/builders/get-aggregated-builder-leaderboard#response-items-rank)

rank

string

The rank position of the builder

[​](https://docs.polymarket.com/api-reference/builders/get-aggregated-builder-leaderboard#response-items-builder)

builder

string

The builder name or identifier

[​](https://docs.polymarket.com/api-reference/builders/get-aggregated-builder-leaderboard#response-items-volume)

volume

number

Total trading volume attributed to this builder

[​](https://docs.polymarket.com/api-reference/builders/get-aggregated-builder-leaderboard#response-items-active-users)

activeUsers

integer

Number of active users for this builder

[​](https://docs.polymarket.com/api-reference/builders/get-aggregated-builder-leaderboard#response-items-verified)

verified

boolean

Whether the builder is verified

[​](https://docs.polymarket.com/api-reference/builders/get-aggregated-builder-leaderboard#response-items-builder-logo)

builderLogo

string

URL to the builder's logo image

[Get trader leaderboard rankings](https://docs.polymarket.com/api-reference/core/get-trader-leaderboard-rankings) [Get daily builder volume time-series](https://docs.polymarket.com/api-reference/builders/get-daily-builder-volume-time-series)

Ctrl+I

Assistant

Responses are generated using AI and may contain mistakes.