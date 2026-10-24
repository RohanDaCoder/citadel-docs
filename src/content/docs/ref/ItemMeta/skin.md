---
title: "itemMeta.skin"
description: 'The face a "player_head" item shows: a player''s name, or the raw textures property'
---

Part of [`itemMeta`](/ref/ItemMeta/).

```luau
itemMeta.skin: (string | { value: string, signature: string ? })?
```

The face a "player_head" item shows: a player's name, or the raw `textures` property. On any other item it is an error.
