---
title: "blockAt.data"
description: "What this block remembers beyond its state; kept with the position, saved with the chunk, and gone when the block goes"
---

Part of [`blockAt`](/ref/BlockAt/).

```luau
blockAt.data: DataView
```

What this block remembers beyond its state; kept with the position, saved with the chunk, and gone when the block goes. Nested writes are tracked; whole-record assignment is supported. Copy before keeping it beyond the hook.
