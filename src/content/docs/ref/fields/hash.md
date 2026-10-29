---
title: 'fields.hash'
description: 'One number 0..1 for each square of cell blocks (1).'
---

Part of [`fields`](/ref/fields/).

```luau
fields.hash(cell: number ?, seed: number ?) → Field
```

One number 0..1 for each square of `cell` blocks (1).

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `cell` | `number` | no |
| `seed` | `number` | no |

## Returns

- [`Field`](/ref/Field/)

## Used in

> "fields.hash(cell, seed)                     -- one number 0 .. 1 for each square of `cell` blocks" — [Blocks and terrain](/world/terrain-generation/)
> "`{ "stone", "andesite", by = fields.hash(3) * 2 }`. `floor(by)` counts" — [Blocks and terrain](/world/terrain-generation/)
