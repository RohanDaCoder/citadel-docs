---
title: 'field:at'
description: 'This field read dx, dy, dz blocks away: fields.water:at(1, 0, 0) is the water east of here.'
---

Part of [`Field`](/ref/Field/).

```luau
field:at(dx: number, dy: number, dz: number) → Field
```

This field read `dx, dy, dz` blocks away: `fields.water:at(1, 0, 0)` is the water east of here.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `dx` | `number` | yes |
| `dy` | `number` | yes |
| `dz` | `number` | yes |

## Returns

- [`Field`](/ref/Field/)
