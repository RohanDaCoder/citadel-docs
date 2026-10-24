---
title: "entityHandle.velocity"
description: "Where it is, live; writing it is a teleport"
---

Part of [`entityHandle`](/ref/EntityHandle/).

```luau
entityHandle.velocity: Vec3 ?
```

Where it is, live; writing it is a teleport. Nil once it is gone. Partial writes preserve other angles; nil after removal. Bodies have no roll. How it is moving, live; writing it is steering by hand. Nil once it is gone. writing it is steering by hand
