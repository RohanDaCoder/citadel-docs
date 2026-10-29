---
title: "world.on_entity_spawn"
url: /docs/citadel/reference/World/on_entity_spawn
---

# world.on_entity_spawn

Tells after a mob appeared, with its handle and name; a natural spawn fires it on every game version that has one, and a pack's own `world.spawn("cow", pos)` fires it too. Mob kinds only.

```
world.on_entity_spawn(fn: (entity: EntityHandle, name: string) -> ()) → Connection
```


## Parameters


## Returns


## Used in
- [`world.on_entity_spawn(function(entity, name) end) -> connection -- a mob appeared; entity is the handle`Game events](/docs/citadel/game-events)
- [``world.on_entity_spawn` fires for mob kinds only. `world.on_entity_death``Game events](/docs/citadel/game-events)
