---
title: 'world.paste'
description: 'Live, stored and sent; air is skipped unless air is true.'
---

Part of [`world`](/ref/World/).

```luau
world.paste(schem: Schematic, origin: Vec3, opts: { air: boolean ?, part: string ? }?)
```

Live, stored and sent; air is skipped unless `air` is true.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `schem` | [`Schematic`](/ref/Schematic/) | yes |
| `origin` | [`Vec3`](/ref/Vec3/) | yes |
| `opts` | `{ air: boolean ?, part: string ? }` | no |

## Used in

> "world.paste(schem, origin)                -- live, like world.fill; { part = "house" } names the paste" — [Blocks and terrain](/world/terrain-generation/)
> "world.paste(road, vec3(0, 64, 0))             -- road.min lands here" — [Blocks and terrain](/world/terrain-generation/)
