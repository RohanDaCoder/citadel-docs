---
title: 'modelPart:part'
description: 'Makes a child part of this one; it turns around pivot, the model''s origin unless you give one.'
---

Part of [`ModelPart`](/ref/ModelPart/).

```luau
modelPart:part(name: string, opts: { pivot: Vec3 ? }?) → ModelPart
```

Makes a child part of this one; it turns around `pivot`, the model's origin unless you give one.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `name` | `string` | yes |
| `opts` | `{ pivot: Vec3 ? }` | no |

## Returns

- [`ModelPart`](/ref/ModelPart/)
