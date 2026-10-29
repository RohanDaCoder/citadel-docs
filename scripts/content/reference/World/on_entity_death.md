---
title: "world.on_entity_death"
url: /docs/citadel/reference/World/on_entity_death
---

# world.on_entity_death

Tells after a mob died; it is gone, so its id and name is all there is. Mob kinds only.

```
world.on_entity_death(fn: (id: number, name: string) -> ()) → Connection
```


## Parameters


## Returns


## Used in
- [`- At 0 health it dies as a mob: it falls over, leaves its `drops`, and is gone a second later. `on_remove` gets `"killed"`, and `world.on_entity_death` fires.`Custom entities](/docs/citadel/custom-entities)
- [`world.on_entity_death(function(id, name) end) -> connection -- a mob died; it is gone, so id and name is all there is`Game events](/docs/citadel/game-events)
- [``world.on_entity_spawn` fires for mob kinds only. `world.on_entity_death``Game events](/docs/citadel/game-events)
