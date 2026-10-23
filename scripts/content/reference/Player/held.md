---
title: "player:held"
url: /docs/citadel/reference/Player/held
---

# player:held

Returns the stack in hand ({ item, count }, plus `id` for a pack item and `damage` for a worn tool), or nil.

```
player:held() → InventorySlot?
```


## Returns


## Used in
- [`player:held() -- { item = "cobblestone", count = 3 } in hand, or nil; a pack item adds `id`, a worn tool `damage``Players](/docs/citadel/players)
- [`player:held() -- { item = "brick", count = 1, id = "copper_ingot" }`Items](/docs/citadel/items)
