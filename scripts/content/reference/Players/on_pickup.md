---
title: "players.on_pickup"
url: /docs/citadel/reference/Players/on_pickup
---

# players.on_pickup

A stack taken off the ground, and one that landed on it. `player` is nil where the world dropped it, or where they have already left.

```
players.on_pickup(fn: (player: Player?, item: string, count: number) -> ()) → Connection
```


## Parameters


## Returns


## Used in
- [`players.on_pickup(function(player, item, count) end) -> connection`Game events](/docs/citadel/game-events)
