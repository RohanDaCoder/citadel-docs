---
title: "players.on_drop"
url: /docs/citadel/reference/Players/on_drop
---

# players.on_drop

Calls `fn` when a stack lands on the ground; `player` is nil where the world dropped it or they have left.

```
players.on_drop(fn: (player: Player?, item: string, count: number) -> ()) → Connection
```


## Parameters


## Returns


## Used in
- [`players.on_drop(function(player, item, count) end) -> connection`Game events](/docs/citadel/game-events)
