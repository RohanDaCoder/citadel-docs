---
title: "player:count"
url: /docs/citadel/reference/Player/count
---

# player:count

Returns how many of an item the player carries, across every slot.

```
player:count(item: ItemMatch) → number
```


## Parameters


## Returns


## Used in
- [`player:count("iron_ingot") -- how many of one item, across every slot; see "items of your own" for what matches`Players](/docs/citadel/players)
- [``player:give`, `player:take`, `player:inventory` and `player:count` work on`Players](/docs/citadel/players)
- [`player:count({ id = "copper_ingot" }) -- every copper ingot they carry`Items](/docs/citadel/items)
- [`player:count("brick") -- plain bricks only, never a copper ingot`Items](/docs/citadel/items)
