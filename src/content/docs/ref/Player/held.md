---
title: 'player:held'
description: 'Returns the stack in hand ({ item, count }, plus id for a pack item and damage for a worn tool), or nil.'
---

Part of [`Player`](/ref/Player/).

```luau
player:held() → InventorySlot ?
```

Returns the stack in hand ({ item, count }, plus `id` for a pack item and `damage` for a worn tool), or nil.

## Returns

- [`InventorySlot`](/ref/InventorySlot/)

## Used in

> "player:held()          -- { item = "cobblestone", count = 3 } in hand, or nil; a pack item adds `id`, a worn tool `damage`" — [Players](/players/player-lifecycle/)
> "player:held()                            -- { item = "brick", count = 1, id = "copper_ingot" }" — [Items](/players/inventory/)
