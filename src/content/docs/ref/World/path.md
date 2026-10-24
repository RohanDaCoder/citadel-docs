---
title: "world.path"
description: "The points a body walks from from to the block at to, or nil"
---

Part of [`world`](/ref/World/).

```luau
world.path(from: Vec3, to: Vec3, opts: { size: (number | { number })?, swim: boolean ?, fall: number ?, range: number ?, budget: number ? }?) → { Vec3 }?
```

The points a body walks from `from` to the block at `to`, or nil. The game's own search: a step up of one block, falls of `fall` (3). `size` is { width, height } (0.6, 1.8); `swim` goes through water; `range` (the distance + 16) and `budget` (2000 nodes) stop a long search, which then gives the part that came closest.

## Parameters

| Name   | Type                                                                                                     | Required |
| ------ | -------------------------------------------------------------------------------------------------------- | -------- |
| `from` | [`Vec3`](/ref/Vec3/)                                                                                     | yes      |
| `to`   | [`Vec3`](/ref/Vec3/)                                                                                     | yes      |
| `opts` | `{ size: ( number \| { number })?, swim: boolean ?, fall: number ?, range: number ?, budget: number ? }` | no       |

## Returns

- `{ Vec3 }?`

## Used in

> "need. It turns smoothly, follows the points of `world.path`, jumps when a" — [Custom entities](/entities/custom-entities/)
> "-- Body i of `b` walks the route { points = world.path(...), at = 1 }." — [Custom entities](/entities/custom-entities/)
> "world.path(from, to, { size = { 0.6, 1.95 } }) -- the points a body walks, a list of vec3, or nil" — [Zones and raycasts](/world/spatial-queries/)
> "- `world.path(from, to, opts)` is the game's own search for a mob: four ways" — [Zones and raycasts](/world/spatial-queries/)
