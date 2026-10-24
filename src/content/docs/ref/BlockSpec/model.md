---
title: "blockSpec.model"
description: "Its own shape on 1.21.4+, in place of texture: a model that stays inside the block, one for every state or one per state"
---

Part of [`blockSpec`](/ref/BlockSpec/).

```luau
blockSpec.model: (Model | { Model })?
```

Its own shape on 1.21.4+, in place of `texture`: a model that stays inside the block, one for every state or one per state. The block collides as its `looks` block does: "rail" is walked through.
