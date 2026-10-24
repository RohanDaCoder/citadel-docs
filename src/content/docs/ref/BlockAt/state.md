---
title: "blockAt.state"
description: "Which of this definition's states it is in, counting from 1"
---

Part of [`blockAt`](/ref/BlockAt/).

```luau
blockAt.state: number
```

Which of this definition's states it is in, counting from 1. Writable, and bounds-checked against the definition's own `looks` list: it _is_ the block state, so a crop's stages cost nothing.
