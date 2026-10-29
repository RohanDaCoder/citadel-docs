---
title: "items.define"
url: /docs/citadel/reference/Items/define
---

# items.define

Load-time only. Hands back the item table: give it, match it, craft it.

```
items.define(spec: { name: string, texture: TextureRef?, label: Text?, lore: ({ Text } | Text)?, looks: string?, stack: number?, glint: boolean?, }) → ItemTable
```


## Parameters


## Returns


## Used in
- [`Set `texture` in `game.items.define` and `game.blocks.define` (below). The`Packs](/docs/citadel/packs)
- [``game.items.define` sets it. Set it by hand only for a file you shipped in`Items](/docs/citadel/items)
- [``game.items.define` returns an item table for anywhere an item goes:`Items](/docs/citadel/items)
