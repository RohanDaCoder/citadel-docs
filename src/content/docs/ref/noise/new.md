---
title: 'noise.new'
description: 'Returns a noise'
---

Part of [`noise`](/ref/noise/).

```luau
noise.new(opts: { seed: number ?, scale: number ?, octaves: number ?, gain: number ?, lacunarity: number ? }?) → Noise
```

Returns a noise. `scale` is the size of a hill in blocks (64), and each of the `octaves` (1) adds detail `lacunarity` (2) times finer and `gain` (0.5) times as strong.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `opts` | `{ seed: number ?, scale: number ?, octaves: number ?, gain: number ?, lacunarity: number ? }` | no |

## Returns

- [`Noise`](/ref/Noise/)

## Used in

> "local hills = noise.new { seed = 7, scale = 96, octaves = 4 }" — [Blocks and terrain](/world/terrain-generation/)
> "local hills = noise.new { seed = 7, scale = 96, octaves = 4 }" — [Blocks and terrain](/world/terrain-generation/)
