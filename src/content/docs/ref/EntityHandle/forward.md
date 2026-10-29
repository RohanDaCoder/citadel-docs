---
title: 'entityHandle.forward'
description: 'The intent fields: what a body wants to do, which is what steering is'
---

Part of [`entityHandle`](/ref/EntityHandle/).

```luau
entityHandle.forward: number
```

The intent fields: what a body *wants* to do, which is what steering is. Writing one outside `on_steer` lasts until the next decision.
