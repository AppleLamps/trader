---
url: "https://docs.polymarket.com/api-reference/tags/get-related-tags-relationships-by-tag-slug"
title: "Get related tags (relationships) by tag slug - Polymarket Documentation"
---

[Skip to main content](https://docs.polymarket.com/api-reference/tags/get-related-tags-relationships-by-tag-slug#content-area)

[Polymarket Documentation home page![light logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-black.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=aff81820f1f3d577fecb3956a8a3bee1)![dark logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-white.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=3bc6857b5dbe8b74b9a7d40975c19b2b)](https://docs.polymarket.com/)

Search...

Ctrl K

Search...

Navigation

Tags

Get related tags (relationships) by tag slug

[User Guide](https://docs.polymarket.com/polymarket-learn/get-started/what-is-polymarket) [For Developers](https://docs.polymarket.com/quickstart/overview) [Changelog](https://docs.polymarket.com/changelog/changelog)

Get related tags (relationships) by tag slug

cURL

Copy

```
curl --request GET \
  --url https://gamma-api.polymarket.com/tags/slug/{slug}/related-tags
```

200

Copy

```
[\
  {\
    "id": "<string>",\
    "tagID": 123,\
    "relatedTagID": 123,\
    "rank": 123\
  }\
]
```

GET

/

tags

/

slug

/

{slug}

/

related-tags

Try it

Get related tags (relationships) by tag slug

cURL

Copy

```
curl --request GET \
  --url https://gamma-api.polymarket.com/tags/slug/{slug}/related-tags
```

200

Copy

```
[\
  {\
    "id": "<string>",\
    "tagID": 123,\
    "relatedTagID": 123,\
    "rank": 123\
  }\
]
```

#### Path Parameters

[​](https://docs.polymarket.com/api-reference/tags/get-related-tags-relationships-by-tag-slug#parameter-slug)

slug

string

required

#### Query Parameters

[​](https://docs.polymarket.com/api-reference/tags/get-related-tags-relationships-by-tag-slug#parameter-omit-empty)

omit\_empty

boolean

[​](https://docs.polymarket.com/api-reference/tags/get-related-tags-relationships-by-tag-slug#parameter-status)

status

enum<string>

Available options:

`active`,

`closed`,

`all`

#### Response

200 - application/json

Related tag relationships

[​](https://docs.polymarket.com/api-reference/tags/get-related-tags-relationships-by-tag-slug#response-items-id)

id

string

[​](https://docs.polymarket.com/api-reference/tags/get-related-tags-relationships-by-tag-slug#response-items-tag-id-one-of-0)

tagID

integer \| null

[​](https://docs.polymarket.com/api-reference/tags/get-related-tags-relationships-by-tag-slug#response-items-related-tag-id-one-of-0)

relatedTagID

integer \| null

[​](https://docs.polymarket.com/api-reference/tags/get-related-tags-relationships-by-tag-slug#response-items-rank-one-of-0)

rank

integer \| null

[Get related tags (relationships) by tag id](https://docs.polymarket.com/api-reference/tags/get-related-tags-relationships-by-tag-id) [Get tags related to a tag id](https://docs.polymarket.com/api-reference/tags/get-tags-related-to-a-tag-id)

Ctrl+I

Assistant

Responses are generated using AI and may contain mistakes.