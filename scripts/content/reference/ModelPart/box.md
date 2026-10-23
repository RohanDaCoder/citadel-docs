---
title: "modelPart:box"
url: /docs/citadel/reference/ModelPart/box
---

# modelPart:box

Corners in any order; a box turns on one axis, in steps of 22.5 up to 45, and `pivot` is the box's own centre unless you give one.

```
modelPart:box(from: Vec3, to: Vec3, skin: ModelSkin, opts: { rotation: Vec3?, pivot: Vec3?, faces: { [Face]: ModelSkin }?, }?)
```


## Parameters
