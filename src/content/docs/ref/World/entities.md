---
title: "world.entities"
description: "Live and queued entities, in ascending id"
---

Part of [`world`](/ref/World/).

```luau
world.entities(query: { near: Vec3 ?, radius: number ?, kind: string ?, mob: boolean ? }?) → { EntityHandle }
```

Live and queued entities, in ascending id. Optional near/radius select a sphere; kind filters by canonical name. near and radius go together. `mob = true` gives the mobs only, `mob = false` the rest.

## Parameters

| Name    | Type                                                                 | Required |
| ------- | -------------------------------------------------------------------- | -------- |
| `query` | `{ near: Vec3 ?, radius: number ?, kind: string ?, mob: boolean ? }` | no       |

## Returns

- `{ EntityHandle }`

## Used in

> "for _, it in world.entities { near = vec3(at.x + 0.5, at.y + 1, at.z + 0.5), radius = 1.5 } do" — [Custom blocks](/world/custom-blocks/)
> "`world.entities`, as well as handles passed to hooks." — [Custom blocks](/world/custom-blocks/)
> "entity here: players are in `players`, never in `world.entities`. `game.entities.<kind>`" — [Game data](/world/game-data/)
> "world.entities { mob = true } -- every mob in this room, as handles" — [Mobs and drops](/entities/mobs/)
> "world.entities { mob = false } -- every entity that is not a mob" — [Mobs and drops](/entities/mobs/)
> "\| `id` \| the entity id, as `e.id` and `world.entities()` give it \|" — [Custom entities](/entities/custom-entities/)
