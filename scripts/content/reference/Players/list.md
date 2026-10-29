---
title: "players.list"
url: /docs/citadel/reference/Players/list
---

# players.list

Returns every player in the room.

```
players.list() → { Player }
```


## Returns


## Used in
- [`local list = players.list()`Guide: Coin rush](/docs/citadel/guides/coin-rush)
- [`for _, p in players.list() do`Guide: Coin rush](/docs/citadel/guides/coin-rush)
- [`for _, p in players.list() do`Scoreboard with a button](/docs/citadel/scoreboard-with-a-button)
- [`players.list() -- array of player`Players](/docs/citadel/players)
- [`for _, a in players.list() do`Players](/docs/citadel/players)
- [`for _, player in players.list() do`Shop](/docs/citadel/shop)
- [`if me and me.id then network.status{ open = math.max(0, me.slots - #players.list()), status = "waiting" } end`Network](/docs/citadel/network)
