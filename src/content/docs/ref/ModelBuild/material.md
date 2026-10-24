---
title: "modelBuild:material"
description: "Makes a named colour a display may repaint; grain (0 to 1) darkens pixels into four tones, alpha below 1 is glass."
---

Part of [`ModelBuild`](/ref/ModelBuild/).

```luau
modelBuild:material(name: string, color: Ink, opts: { grain: number ?, alpha: number ? }?) → ModelMaterial
```

Makes a named colour a display may repaint; `grain` (0 to 1) darkens pixels into four tones, `alpha` below 1 is glass.

## Parameters

| Name    | Type                                   | Required |
| ------- | -------------------------------------- | -------- |
| `name`  | `string`                               | yes      |
| `color` | [`Ink`](/ref/Ink/)                     | yes      |
| `opts`  | `{ grain: number ?, alpha: number ? }` | no       |

## Returns

- [`ModelMaterial`](/ref/ModelMaterial/)
