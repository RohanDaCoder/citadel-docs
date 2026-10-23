---
title: "world.entities"
url: /docs/citadel/reference/World/entities
---

# world.entities

Live and queued entities, in ascending id. Optional near/radius select a sphere; kind filters by canonical name. near and radius go together. `mob = true` gives the mobs only, `mob = false` the rest.

```
world.entities(query: { near: Vec3?, radius: number?, kind: string?, mob: boolean? }?) → { EntityHandle }
```


## Parameters


## Returns


## Used in
- [`for _, it in world.entities { near = vec3(at.x + 0.5, at.y + 1, at.z + 0.5), radius = 1.5 } do`Custom blocks](/docs/citadel/custom-blocks)
- [``world.entities`, as well as handles passed to hooks.`Custom blocks](/docs/citadel/custom-blocks)
- [`entity here: players are in `players`, never in `world.entities`. `game.entities.<kind>``Game data](/docs/citadel/game-data)
- [`world.entities { mob = true } -- every mob in this room, as handles`Mobs and drops](/docs/citadel/mobs-and-drops)
- [`world.entities { mob = false } -- every entity that is not a mob`Mobs and drops](/docs/citadel/mobs-and-drops)
- [`| `id` | the entity id, as `e.id` and `world.entities()` give it |`Custom entities](/docs/citadel/custom-entities)
- [``world.spawn` returns a handle, `world.entities()` lists handles, and each`Custom entities](/docs/citadel/custom-entities)
