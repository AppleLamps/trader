---
url: "https://docs.polymarket.com/api-reference/builders/get-daily-builder-volume-time-series"
title: "Get daily builder volume time-series - Polymarket Documentation"
---

[Skip to main content](https://docs.polymarket.com/api-reference/builders/get-daily-builder-volume-time-series#content-area)

[Polymarket Documentation home page![light logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-black.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=aff81820f1f3d577fecb3956a8a3bee1)![dark logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-white.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=3bc6857b5dbe8b74b9a7d40975c19b2b)](https://docs.polymarket.com/)

Search...

Ctrl K

Search...

Navigation

Builders

Get daily builder volume time-series

[User Guide](https://docs.polymarket.com/polymarket-learn/get-started/what-is-polymarket) [For Developers](https://docs.polymarket.com/quickstart/overview) [Changelog](https://docs.polymarket.com/changelog/changelog)

Get daily builder volume time-series

cURL

Copy

```
curl --request GET \
  --url 'https://data-api.polymarket.com/v1/builders/volume?timePeriod=DAY'
```

200

400

500

Copy

```
[\
  {\
    "dt": "2025-11-15T00:00:00Z",\
    "builder": "<string>",\
    "builderLogo": "<string>",\
    "verified": true,\
    "volume": 123,\
    "activeUsers": 123,\
    "rank": "<string>"\
  }\
]
```

GET

/

v1

/

builders

/

volume

Try it

Get daily builder volume time-series

cURL

Copy

```
curl --request GET \
  --url 'https://data-api.polymarket.com/v1/builders/volume?timePeriod=DAY'
```

200

400

500

Copy

```
[\
  {\
    "dt": "2025-11-15T00:00:00Z",\
    "builder": "<string>",\
    "builderLogo": "<string>",\
    "verified": true,\
    "volume": 123,\
    "activeUsers": 123,\
    "rank": "<string>"\
  }\
]
```

#### Query Parameters

[​](https://docs.polymarket.com/api-reference/builders/get-daily-builder-volume-time-series#parameter-time-period)

timePeriod

enum<string>

default:DAY

The time period to fetch daily records for.

Available options:

`DAY`,

`WEEK`,

`MONTH`,

`ALL`

#### Response

200

application/json

Success - Returns array of daily volume records

[​](https://docs.polymarket.com/api-reference/builders/get-daily-builder-volume-time-series#response-items-dt)

dt

string<date-time>

The timestamp for this volume entry in ISO 8601 format

Example:

`"2025-11-15T00:00:00Z"`

[​](https://docs.polymarket.com/api-reference/builders/get-daily-builder-volume-time-series#response-items-builder)

builder

string

The builder name or identifier

[​](https://docs.polymarket.com/api-reference/builders/get-daily-builder-volume-time-series#response-items-builder-logo)

builderLogo

string

URL to the builder's logo image

[​](https://docs.polymarket.com/api-reference/builders/get-daily-builder-volume-time-series#response-items-verified)

verified

boolean

Whether the builder is verified

[​](https://docs.polymarket.com/api-reference/builders/get-daily-builder-volume-time-series#response-items-volume)

volume

number

Trading volume for this builder on this date

[​](https://docs.polymarket.com/api-reference/builders/get-daily-builder-volume-time-series#response-items-active-users)

activeUsers

integer

Number of active users for this builder on this date

[​](https://docs.polymarket.com/api-reference/builders/get-daily-builder-volume-time-series#response-items-rank)

rank

string

The rank position of the builder on this date

[Get aggregated builder leaderboard](https://docs.polymarket.com/api-reference/builders/get-aggregated-builder-leaderboard) [Overview](https://docs.polymarket.com/developers/misc-endpoints/bridge-overview)

Ctrl+I

Assistant

Responses are generated using AI and may contain mistakes.