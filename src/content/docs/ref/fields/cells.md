---
title: "fields.cells"
description: "A scattered grid, one point per size blocks: the distance to the nearest point, and that point's own number 0..1."
---

Part of [`fields`](/ref/fields/).

```luau
fields.cells(size: number, seed: number ?) → { distance: Field, random: Field }
```

A scattered grid, one point per `size` blocks: the distance to the nearest point, and that point's own number 0..1.

## Parameters

| Name   | Type     | Required |
| ------ | -------- | -------- |
| `size` | `number` | yes      |
| `seed` | `number` | no       |

## Returns

- `{ distance: Field , random: Field }`

## Used in

> "fields.cells(size, seed) -- { distance = field, random = field }: the nearest point of a scattered grid" — [Blocks and terrain](/world/terrain-generation/)
