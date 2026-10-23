---
title: 'modelPart:hitbox'
description: 'A box a player can hit on a living body that wears the model (clients from 1.19.4)'
---

Part of [`ModelPart`](/ref/ModelPart/).

```luau
modelPart:hitbox(from: Vec3, to: Vec3)
```

A box a player can hit on a living body that wears the model (clients from 1.19.4). Not drawn; corners in any order, in model units. Square from above (its longer side), so split a long part. Animations do not move it. A model with none is hit on one box of the body's `size`.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `from` | [`Vec3`](/ref/Vec3/) | yes |
| `to` | [`Vec3`](/ref/Vec3/) | yes |
