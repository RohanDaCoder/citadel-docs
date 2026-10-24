---
title: 'modelBuild:part'
description: 'Makes a named child part of the root that turns around its pivot, the model''s origin unless given.'
---

Part of [`ModelBuild`](/ref/ModelBuild/).

```luau
modelBuild:part(name: string, opts: { pivot: Vec3 ? }?) → ModelPart
```

Makes a named child part of the root that turns around its `pivot`, the model's origin unless given.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `name` | `string` | yes |
| `opts` | `{ pivot: Vec3 ? }` | no |

## Returns

- [`ModelPart`](/ref/ModelPart/)
