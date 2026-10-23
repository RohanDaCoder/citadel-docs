---
title: "player:take"
url: /docs/citadel/reference/Player/take
---

# player:take

Up to `count` (1 unless you say) of what matches, the hand first; answers how many it took.

```
player:take(item: ItemMatch, count: number?) → number
```


## Parameters


## Returns


## Used in
- [`player:take("coal", 8) -- takes up to 8, the hand first; answers how many it took`Players](/docs/citadel/players)
- [``player:give`, `player:take`, `player:inventory` and `player:count` work on`Players](/docs/citadel/players)
- [`player:take({ id = "copper_ingot" }, 2) -- up to 2 of them; answers how many it took`Items](/docs/citadel/items)
- [`player:take(COPPER, 2) -- an item table matches by its id`Items](/docs/citadel/items)
