---
title: 'world.explode'
description: 'A blast at a point'
---

Part of [`world`](/ref/World/).

```luau
world.explode(pos: Vec3, power: number ?)
```

A blast at a point. The power is clamped by this game's own column and the tick's explosion budget decides when it goes off, never whether.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `pos` | [`Vec3`](/ref/Vec3/) | yes |
| `power` | `number` | no |

## Used in

> "- A blast of TNT, of a bed and of `world.explode` has no kind. It follows the" — [Game data](/world/game-data/)
> "world.explode(at, 4)" — [Custom entities](/entities/custom-entities/)
