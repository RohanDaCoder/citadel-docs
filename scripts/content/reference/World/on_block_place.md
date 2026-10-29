---
title: "world.on_block_place"
url: /docs/citadel/reference/World/on_block_place
---

# world.on_block_place

Tells after a block was placed, with its canonical name. Observe-only; `player` is nil when nobody placed it or they left.

```
world.on_block_place(fn: (player: Player?, pos: Vec3, block: string) -> ()) → Connection
```


## Parameters


## Returns


## Used in
- [`world.on_block_place(function(player, pos, block) end) -> connection`Game events](/docs/citadel/game-events)
- [``world.on_block_break` or `world.on_block_place`.`Cancelling events](/docs/citadel/cancelling-events)
