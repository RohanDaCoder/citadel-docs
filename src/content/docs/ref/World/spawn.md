---
title: "world.spawn"
description: "Puts an entity at a point and returns its handle"
---

Part of [`world`](/ref/World/).

```luau
world.spawn(def: EntityDef | string, pos: Vec3, data: { [string]: any }?) → EntityHandle ?
```

Puts an entity at a point and returns its handle. A mob kind of the game by name (`world.spawn("cow", pos)`) is the game's own entity, and takes no `data`. A pack's own kind takes the data it starts life holding. `nil` for a kind nothing defined and this game does not have.

## Parameters

| Name   | Type                  | Required |
| ------ | --------------------- | -------- |
| `def`  | `EntityDef \| string` | yes      |
| `pos`  | [`Vec3`](/ref/Vec3/)  | yes      |
| `data` | `{ [ string ]: any }` | no       |

## Returns

- [`EntityHandle`](/ref/EntityHandle/)

## Used in

> "assigning the whole record again. This works on handles from `world.spawn` and" — [Custom blocks](/world/custom-blocks/)
> "`mob = false`. Pass it to `world.spawn` just like the handle from `define`." — [Game data](/world/game-data/)
> "- `false` stops natural spawning only. A spawner block, `world.spawn`," — [Game data](/world/game-data/)
> "\| Physics, gameplay hooks or persistence \| `game.entities.define` and `world.spawn` \| Gives a body behavior independent of its appearance. \|" — [Displays](/ui/displays/)
> "local c = world.spawn(car, vec3(0.5, 65, 0.5))" — [Displays](/ui/displays/)
> "its normal drops. `world.spawn` with the name of a mob kind spawns one and" — [Mobs and drops](/entities/mobs/)
