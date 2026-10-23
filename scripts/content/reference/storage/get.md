---
title: "storage.get"
url: /docs/citadel/reference/storage/get
---

# storage.get

Returns the value saved under `key`, or nil when there is none.

```
storage.get(key: string) → any
```


## Parameters


## Returns


## Used in
- [`local best = storage.get("best." .. player.uuid) or 0`Guide: Coin rush](/docs/citadel/guides/coin-rush)
- [`if p.data.coins > (storage.get(key) or 0) then`Guide: Coin rush](/docs/citadel/guides/coin-rush)
- [`local best = storage.get("best." .. player.uuid)`Guide: Parkour, a room each](/docs/citadel/guides/parkour-a-room-each)
- [`local best = storage.get(key)`Guide: Parkour, a room each](/docs/citadel/guides/parkour-a-room-each)
- [`local score = storage.get("taps." .. p.name) or 0`Scoreboard with a button](/docs/citadel/scoreboard-with-a-button)
- [`storage.set(key, (storage.get(key) or 0) + 1)`Scoreboard with a button](/docs/citadel/scoreboard-with-a-button)
- [`local best = storage.get("best." .. player.name) or 0`Storage](/docs/citadel/storage)
