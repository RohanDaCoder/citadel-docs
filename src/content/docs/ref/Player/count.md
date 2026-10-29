---
title: 'player:count'
description: 'Returns how many of an item the player carries, across every slot.'
---

Part of [`Player`](/ref/Player/).

```luau
player:count(item: ItemMatch) → number
```

Returns how many of an item the player carries, across every slot.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `item` | [`ItemMatch`](/ref/ItemMatch/) | yes |

## Returns

- `number`

## Used in

> "player:count("iron_ingot")  -- how many of one item, across every slot; see "items of your own" for what matches" — [Players](/players/player-lifecycle/)
> "`player:give`, `player:take`, `player:inventory` and `player:count` work on" — [Players](/players/player-lifecycle/)
> "player:count({ id = "copper_ingot" })    -- every copper ingot they carry" — [Items](/players/inventory/)
> "player:count("brick")                    -- plain bricks only, never a copper ingot" — [Items](/players/inventory/)
