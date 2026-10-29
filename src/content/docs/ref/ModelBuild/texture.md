---
title: 'modelBuild:texture'
description: 'Makes a pixel picture for one face; with tint, drawn in greys and coloured by that material'
---

Part of [`ModelBuild`](/ref/ModelBuild/).

```luau
modelBuild:texture(width: number, height: number, opts: { tint: ModelMaterial ?, scroll: ("up" | "down" | "left" | "right")?, speed: number ? }?) → ModelTexture
```

Makes a pixel picture for one face; with `tint`, drawn in greys and coloured by that material. With `scroll`, it moves by itself on a block drawn from the model, `speed` texels a tick (1, 2, 3, or 0.5, 0.25).

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `width` | `number` | yes |
| `height` | `number` | yes |
| `opts` | `{ tint: ModelMaterial ?, scroll: ( "up" \| "down" \| "left" \| "right" )?, speed: number ? }` | no |

## Returns

- [`ModelTexture`](/ref/ModelTexture/)
