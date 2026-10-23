---
title: "world.on_block_break"
url: /docs/citadel/reference/World/on_block_break
---

# world.on_block_break

What the survival tick did. Observe-only: the world has already changed, and what the callback returns is not read.

```
world.on_block_break(fn: (player: Player?, pos: Vec3, block: string) -> ()) → Connection
```


## Parameters


## Returns


## Used in
- [`world.on_block_break(function(player, pos, block) end) -> connection`Game events](/docs/citadel/game-events)
- [`world.on_block_break(function(player, pos, block)`Game events](/docs/citadel/game-events)
- [``world.on_block_break` or `world.on_block_place`.`Cancelling events](/docs/citadel/cancelling-events)
- [`(`world.on_block_break` and the rest).`Limits and reload](/docs/citadel/limits-and-reload)
