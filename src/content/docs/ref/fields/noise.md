---
title: "fields.noise"
description: "Smooth noise, about -1..1"
---

Part of [`fields`](/ref/fields/).

```luau
fields.noise(opts: { seed: number ?, scale: number ?, octaves: number ?, gain: number ?, lacunarity: number ?, solid: boolean ? }?) → Field
```

Smooth noise, about -1..1. `solid = true` changes with y too.

## Parameters

| Name   | Type                                                                                                             | Required |
| ------ | ---------------------------------------------------------------------------------------------------------------- | -------- |
| `opts` | `{ seed: number ?, scale: number ?, octaves: number ?, gain: number ?, lacunarity: number ?, solid: boolean ? }` | no       |

## Returns

- [`Field`](/ref/Field/)

## Used in

> "local hills = fields.noise { seed = 7, scale = 96, octaves = 4 }" — [Blocks and terrain](/world/terrain-generation/)
> "local dry = fields.noise { seed = 8, scale = 300 }:gt(0)" — [Blocks and terrain](/world/terrain-generation/)
