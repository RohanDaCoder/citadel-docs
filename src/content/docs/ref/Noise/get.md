---
title: 'noise:get'
description: 'Returns about -1..1 at a point: get(x, z) for a height map, get(x, y, z) for caves and overhangs.'
---

Part of [`Noise`](/ref/Noise/).

```luau
noise:get(x: number, y_or_z: number, z: number ?) → number
```

Returns about -1..1 at a point: `get(x, z)` for a height map, `get(x, y, z)` for caves and overhangs.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `x` | `number` | yes |
| `y_or_z` | `number` | yes |
| `z` | `number` | no |

## Returns

- `number`
