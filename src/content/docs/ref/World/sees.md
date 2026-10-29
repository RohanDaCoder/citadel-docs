---
title: 'world.sees'
description: 'True when no block stops the line from from to to: a block with a collision box does (glass, leaves), water and grass do not.'
---

Part of [`world`](/ref/World/).

```luau
world.sees(from: Vec3, to: Vec3) → boolean
```

True when no block stops the line from `from` to `to`: a block with a collision box does (glass, leaves), water and grass do not.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `from` | [`Vec3`](/ref/Vec3/) | yes |
| `to` | [`Vec3`](/ref/Vec3/) | yes |

## Returns

- `boolean`

## Used in

> "world.sees(from, to)                 -- true when no block stops the line between the two points" — [Zones and raycasts](/world/spatial-queries/)
> "- `world.sees` and `world.raycasts` look as a mob looks: a block with a" — [Zones and raycasts](/world/spatial-queries/)
