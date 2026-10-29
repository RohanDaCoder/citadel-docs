---
title: 'Noise type'
description: 'Smooth random numbers from noise.new: the same seed gives the same numbers every time.'
---

Smooth random numbers from `noise.new`: the same seed gives the same numbers every time.

## Functions

| Call | Purpose |
| --- | --- |
| [`get`](/ref/Noise/get/) | Returns about -1..1 at a point: `get(x, z)` for a height map, `get(x, y, z)` for caves and overhangs. |
| [`grid`](/ref/Noise/grid/) | Returns `width * depth` heights in one call, row by row: the number for `(x + dx, z + dz)` is at `[dz * width + dx + 1]`. |
