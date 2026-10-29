---
title: "blockSpec.model"
url: /docs/citadel/reference/BlockSpec/model
---

# blockSpec.model

Its own shape on 1.21.4+, in place of `texture`: a model that stays inside the block, one for every state or one per state. The block collides as its `looks` block does: "rail" is walked through.

```
blockSpec.model: (Model | { Model })?
```
