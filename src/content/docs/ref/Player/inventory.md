---
title: "player:inventory"
description: "Returns one { item, count } row per filled slot."
---

Part of [`Player`](/ref/Player/).

```luau
player:inventory() → { InventorySlot }
```

Returns one { item, count } row per filled slot.

## Returns

- `{ InventorySlot }`

## Used in

> "player:inventory() -- { { item = "cobblestone", count = 3 }, ... }, one entry per filled slot, the same rows" — [Players](/players/player-lifecycle/)
> "`player:give`, `player:take`, `player:inventory` and `player:count` work on" — [Players](/players/player-lifecycle/)
