---
title: "generated:sample"
description: "Returns a field's value at a position; nil for a field made after world.generate, or for rules with no height."
---

Part of [`Generated`](/ref/Generated/).

```luau
generated:sample(field: Field | number, pos: Vec3) → number ?
```

Returns a field's value at a position; `nil` for a field made after `world.generate`, or for rules with no `height`.

## Parameters

| Name    | Type                 | Required |
| ------- | -------------------- | -------- |
| `field` | `Field \| number`    | yes      |
| `pos`   | [`Vec3`](/ref/Vec3/) | yes      |

## Returns

- `number ?`
