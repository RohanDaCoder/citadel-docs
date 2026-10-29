---
title: 'fields.mix'
description: 'a where t is 0, b where it is 1.'
---

Part of [`fields`](/ref/fields/).

```luau
fields.mix(a: Field | number, b: Field | number, t: Field | number) → Field
```

`a` where `t` is 0, `b` where it is 1.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `a` | `Field \| number` | yes |
| `b` | `Field \| number` | yes |
| `t` | `Field \| number` | yes |

## Returns

- [`Field`](/ref/Field/)

## Used in

> "fields.mix(a, b, t)                         -- a where t is 0, b where t is 1" — [Blocks and terrain](/world/terrain-generation/)
