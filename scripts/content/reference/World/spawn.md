---
title: "world.spawn"
url: /docs/citadel/reference/World/spawn
---

# world.spawn

Puts an entity at a point and returns its handle. A mob kind of the game by name (`world.spawn("cow", pos)`) is the game's own entity, and takes no `data`. A pack's own kind takes the data it starts life holding. `nil` for a kind nothing defined and this game does not have.

```
world.spawn(def: EntityDef | string, pos: Vec3, data: { [string]: any }?) → EntityHandle?
```


## Parameters


## Returns


## Used in
- [`assigning the whole record again. This works on handles from `world.spawn` and`Custom blocks](/docs/citadel/custom-blocks)
- [``mob = false`. Pass it to `world.spawn` just like the handle from `define`.`Game data](/docs/citadel/game-data)
- [`- `false` stops natural spawning only. A spawner block, `world.spawn`,`Game data](/docs/citadel/game-data)
- [`| Physics, gameplay hooks or persistence | `game.entities.define` and `world.spawn` | Gives a body behavior independent of its appearance. |`Displays](/docs/citadel/displays)
- [`local c = world.spawn(car, vec3(0.5, 65, 0.5))`Displays](/docs/citadel/displays)
- [`its normal drops. `world.spawn` with the name of a mob kind spawns one and`Mobs and drops](/docs/citadel/mobs-and-drops)
- [`local cow = world.spawn("cow", vec3(4.5, 65, 8.5)) -- nil where this game has no such kind`Mobs and drops](/docs/citadel/mobs-and-drops)
- [`local it = world.spawn(rocket, vec3(8.5, 66, 8.5), { fuse = 40 })`Custom entities](/docs/citadel/custom-entities)
