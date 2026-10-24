---
title: "blockSpec.item"
description: "The block in a hand"
---

Part of [`blockSpec`](/ref/BlockSpec/).

```luau
blockSpec.item: (ItemTable | false)?
```

The block in a hand. Its `id` is set to the block's name, so placing it puts this block down, and a break leaves it unless `drops` says. false is no item, also for a block with a texture.
