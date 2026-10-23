---
title: "storage.set"
url: /docs/citadel/reference/storage/set
---

# storage.set

Saves a value under `key` in this pack's storage.json; nil forgets it.

```
storage.set(key: string, value: any)
```


## Parameters


## Used in
- [`storage.set(key, p.data.coins)`Guide: Coin rush](/docs/citadel/guides/coin-rush)
- [`storage.set(key, p.data.coins)`Guide: Coin rush](/docs/citadel/guides/coin-rush)
- [`storage.set(key, t)`Guide: Parkour, a room each](/docs/citadel/guides/parkour-a-room-each)
- [`storage.set(key, t)`Guide: Parkour, a room each](/docs/citadel/guides/parkour-a-room-each)
- [`storage.set(key, (storage.get(key) or 0) + 1)`Scoreboard with a button](/docs/citadel/scoreboard-with-a-button)
- [`- Each write is checked at the assignment by the `storage.set` rules. A`Custom blocks](/docs/citadel/custom-blocks)
- [``ipairs` operations. `storage.set(key, view)` accepts views directly.`Custom blocks](/docs/citadel/custom-blocks)
- [`players.on_leave(function(p) storage.set("coins." .. p.uuid, p.data.coins) end)`Players](/docs/citadel/players)
