---
url: "https://docs.polymarket.com/developers/sports-websocket/message-format"
title: "Message Format - Polymarket Documentation"
---

[Skip to main content](https://docs.polymarket.com/developers/sports-websocket/message-format#content-area)

[Polymarket Documentation home page![light logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-black.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=aff81820f1f3d577fecb3956a8a3bee1)![dark logo](https://mintcdn.com/polymarket-292d1b1b/HmeJ4Y1FlVRRp8nd/images/logo-white.svg?fit=max&auto=format&n=HmeJ4Y1FlVRRp8nd&q=85&s=3bc6857b5dbe8b74b9a7d40975c19b2b)](https://docs.polymarket.com/)

Search...

Ctrl K

Search...

Navigation

Sports Websocket

Message Format

[User Guide](https://docs.polymarket.com/polymarket-learn/get-started/what-is-polymarket) [For Developers](https://docs.polymarket.com/quickstart/overview) [Changelog](https://docs.polymarket.com/changelog/changelog)

On this page

- [sport\_result Message](https://docs.polymarket.com/developers/sports-websocket/message-format#sport_result-message)
- [Structure](https://docs.polymarket.com/developers/sports-websocket/message-format#structure)
- [Example Messages](https://docs.polymarket.com/developers/sports-websocket/message-format#example-messages)
- [Slug Format](https://docs.polymarket.com/developers/sports-websocket/message-format#slug-format)
- [Period Values](https://docs.polymarket.com/developers/sports-websocket/message-format#period-values)
- [Handling Updates](https://docs.polymarket.com/developers/sports-websocket/message-format#handling-updates)

Once connected to the Sports WebSocket, clients receive JSON messages whenever a sports event updates. Messages are broadcast to all connected clients automatically.

* * *

## [​](https://docs.polymarket.com/developers/sports-websocket/message-format\#sport_result-message)  sport\_result Message

Emitted when:

- A match goes live
- The score changes
- The period changes (e.g., halftime, overtime)
- A match ends
- Possession changes (NFL and CFB only)

### [​](https://docs.polymarket.com/developers/sports-websocket/message-format\#structure)  Structure

[​](https://docs.polymarket.com/developers/sports-websocket/message-format#param-game-id)

gameId

number

Unique identifier for the game

[​](https://docs.polymarket.com/developers/sports-websocket/message-format#param-league-abbreviation)

leagueAbbreviation

string

League identifier (e.g., `"nfl"`, `"nba"`, `"cs2"`)

[​](https://docs.polymarket.com/developers/sports-websocket/message-format#param-home-team)

homeTeam

string

Home team name or abbreviation

[​](https://docs.polymarket.com/developers/sports-websocket/message-format#param-away-team)

awayTeam

string

Away team name or abbreviation

[​](https://docs.polymarket.com/developers/sports-websocket/message-format#param-status)

status

string

Game status (e.g., `"InProgress"`, `"finished"`)

[​](https://docs.polymarket.com/developers/sports-websocket/message-format#param-live)

live

boolean

`true` if the match is currently in progress

[​](https://docs.polymarket.com/developers/sports-websocket/message-format#param-ended)

ended

boolean

`true` if the match has concluded

[​](https://docs.polymarket.com/developers/sports-websocket/message-format#param-score)

score

string

Current score (format varies by sport)

[​](https://docs.polymarket.com/developers/sports-websocket/message-format#param-period)

period

string

Current period (e.g., `"Q4"`, `"2H"`, `"2/3"`)

[​](https://docs.polymarket.com/developers/sports-websocket/message-format#param-elapsed)

elapsed

string

Time elapsed in current period (e.g., `"05:09"`)

[​](https://docs.polymarket.com/developers/sports-websocket/message-format#param-finished-timestamp)

finishedTimestamp

string

Timestamp when the match ended (only present when `ended: true`)

[​](https://docs.polymarket.com/developers/sports-websocket/message-format#param-turn)

turn

string

Team abbreviation with possession (NFL/CFB only)

The `turn` field is only present for NFL and CFB games and indicates which team currently has the ball.

### [​](https://docs.polymarket.com/developers/sports-websocket/message-format\#example-messages)  Example Messages

**NFL (in progress):**

Copy

```
{
  "gameId": 19439,
  "leagueAbbreviation": "nfl",
  "homeTeam": "LAC",
  "awayTeam": "BUF",
  "status": "InProgress",
  "score": "3-16",
  "period": "Q4",
  "elapsed": "5:18",
  "live": true,
  "ended": false,
  "turn": "lac"
}
```

**Esports - CS2 (finished):**

Copy

```
{
  "gameId": 1317359,
  "leagueAbbreviation": "cs2",
  "homeTeam": "ARCRED",
  "awayTeam": "The glecs",
  "status": "finished",
  "score": "000-000|2-0|Bo3",
  "period": "2/3",
  "live": false,
  "ended": true
}
```

* * *

## [​](https://docs.polymarket.com/developers/sports-websocket/message-format\#slug-format)  Slug Format

The `slug` field follows a consistent naming convention:

Copy

```
{league}-{team1}-{team2}-{date}
```

**Examples:**

- `nfl-buf-kc-2025-01-26` — NFL: Buffalo Bills vs Kansas City Chiefs
- `nba-lal-bos-2025-02-15` — NBA: LA Lakers vs Boston Celtics
- `mlb-nyy-bos-2025-04-01` — MLB: NY Yankees vs Boston Red Sox

* * *

## [​](https://docs.polymarket.com/developers/sports-websocket/message-format\#period-values)  Period Values

| Period | Description |
| --- | --- |
| `1H` | First half |
| `2H` | Second half |
| `1Q`, `2Q`, `3Q`, `4Q` | Quarters (NFL, NBA) |
| `HT` | Halftime |
| `FT` | Full time (match ended in regulation) |
| `FT OT` | Full time with overtime |
| `FT NR` | Full time, no result (draw or canceled) |
| `End 1`, `End 2`, etc. | End of inning (MLB) |
| `1/3`, `2/3`, `3/3` | Map number in Bo3 series (Esports) |
| `1/5`, `2/5`, etc. | Map number in Bo5 series (Esports) |

* * *

## [​](https://docs.polymarket.com/developers/sports-websocket/message-format\#handling-updates)  Handling Updates

When processing messages, use the `gameId` field as the unique identifier to update your local state:

Copy

```
// Update or insert based on gameId
setSportsData(prev => {
  const existing = prev.find(item => item.gameId === data.gameId);
  if (existing) {
    return prev.map(item =>
      item.gameId === data.gameId ? data : item
    );
  }
  return [...prev, data];
});
```

[Overview](https://docs.polymarket.com/developers/sports-websocket/overview) [Quickstart](https://docs.polymarket.com/developers/sports-websocket/quickstart)

Ctrl+I

Assistant

Responses are generated using AI and may contain mistakes.