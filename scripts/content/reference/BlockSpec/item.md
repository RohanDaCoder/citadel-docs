---
title: "blockSpec.item"
url: /docs/citadel/reference/BlockSpec/item
---

# blockSpec.item

The block in a hand. Its `id` is set to the block's name, so placing it puts this block down, and a break leaves it unless `drops` says. false is no item, also for a block with a texture.

```
blockSpec.item: (ItemTable | false)?
```
