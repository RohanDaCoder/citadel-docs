---
title: "world.raycasts"
description: "n lines at once"
---

Part of [`world`](/ref/World/).

```luau
world.raycasts(rays: buffer, out: buffer, n: number)
```

`n` lines at once. `rays` holds six f64 a line (from x, y, z, to x, y, z); `out` gets one f64 a line: how far along it the first block is that stops it, or -1 for a clear line.

## Parameters

| Name   | Type     | Required |
| ------ | -------- | -------- |
| `rays` | `buffer` | yes      |
| `out`  | `buffer` | yes      |
| `n`    | `number` | yes      |

## Used in

> "world.raycasts(rays, out, n) -- n lines at once, in buffers; see below" — [Zones and raycasts](/world/spatial-queries/)
> "- `world.sees` and `world.raycasts` look as a mob looks: a block with a" — [Zones and raycasts](/world/spatial-queries/)
