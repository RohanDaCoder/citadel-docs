---
title: "modelDisplay.paint"
description: "Whether it is still present"
---

Part of [`modelDisplay`](/ref/ModelDisplay/).

```luau
modelDisplay.paint: { [string]: Ink }
```

Whether it is still present. Read-only. Where it stands; live, and each write is a move of its own. Partial writes preserve other angles; nil after removal. Reads vec3; write a number or equal-axis vec3 for uniform size. Nil when gone. Material name to colour; write-only.
