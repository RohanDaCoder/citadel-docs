---
title: 'blockSpec.extends'
description: 'A handle, a game block''s name, a plain table of fields and hooks, or a list of those innermost first'
---

Part of [`blockSpec`](/ref/BlockSpec/).

```luau
blockSpec.extends: (BlockRef | { [string]: any } | { any })?
```

A handle, a game block's name, a plain table of fields and hooks, or a list of those **innermost first**. There is no class and no metatable: fields merge and hooks wrap.
