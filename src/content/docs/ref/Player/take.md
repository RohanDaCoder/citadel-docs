---
title: "player:take"
description: "Up to count (1 unless you say) of what matches, the hand first; answers how many it took."
---

Part of [`Player`](/ref/Player/).

```luau
player:take(item: ItemMatch, count: number ?) → number
```

Up to `count` (1 unless you say) of what matches, the hand first; answers how many it took.

## Parameters

| Name    | Type                           | Required |
| ------- | ------------------------------ | -------- |
| `item`  | [`ItemMatch`](/ref/ItemMatch/) | yes      |
| `count` | `number`                       | no       |

## Returns

- `number`

## Used in

> "player:take("coal", 8) -- takes up to 8, the hand first; answers how many it took" — [Players](/players/player-lifecycle/)
> "`player:give`, `player:take`, `player:inventory` and `player:count` work on" — [Players](/players/player-lifecycle/)
> "player:take({ id = "copper_ingot" }, 2) -- up to 2 of them; answers how many it took" — [Items](/players/inventory/)
> "player:take(COPPER, 2) -- an item table matches by its id" — [Items](/players/inventory/)
