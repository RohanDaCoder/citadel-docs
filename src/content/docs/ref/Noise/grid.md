---
title: 'noise:grid'
description: 'Returns width  depth heights in one call, row by row: the number for (x + dx, z + dz) is at [dz  width + dx + 1].'
---

Part of [`Noise`](/ref/Noise/).

```luau
noise:grid(x: number, z: number, width: number, depth: number) → { number }
```

Returns `width * depth` heights in one call, row by row: the number for `(x + dx, z + dz)` is at `[dz * width + dx + 1]`.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `x` | `number` | yes |
| `z` | `number` | yes |
| `width` | `number` | yes |
| `depth` | `number` | yes |

## Returns

- `{ number }`
