---
title: 'modelPart:box'
description: 'Corners in any order; a box turns on one axis, in steps of 22.5 up to 45, and pivot is the box''s own centre unless you give one.'
---

Part of [`ModelPart`](/ref/ModelPart/).

```luau
modelPart:box(from: Vec3, to: Vec3, skin: ModelSkin, opts: { rotation: Vec3 ?, pivot: Vec3 ?, faces: { [Face]: ModelSkin }?, }?)
```

Corners in any order; a box turns on one axis, in steps of 22.5 up to 45, and `pivot` is the box's own centre unless you give one.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `from` | [`Vec3`](/ref/Vec3/) | yes |
| `to` | [`Vec3`](/ref/Vec3/) | yes |
| `skin` | [`ModelSkin`](/ref/ModelSkin/) | yes |
| `opts` | `{ rotation: Vec3 ?, pivot: Vec3 ?, faces: { [ Face ]: ModelSkin }?, }` | no |
