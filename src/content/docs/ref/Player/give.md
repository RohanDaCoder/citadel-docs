---
title: "player:give"
description: 'One item: "stone", or { item = "arrow", count = 16 }.'
---

Part of [`Player`](/ref/Player/).

```luau
player:give(item: ItemSpec)
```

One item: "stone", or { item = "arrow", count = 16 }.

## Parameters

| Name   | Type                         | Required |
| ------ | ---------------------------- | -------- |
| `item` | [`ItemSpec`](/ref/ItemSpec/) | yes      |

## Used in

> "player:give(macerator.item)" — [Custom blocks](/world/custom-blocks/)
> "player:give(macerator.item) -- a Macerator; place it and it is one" — [Custom blocks](/world/custom-blocks/)
> "if game.item("bucket") then player:give("bucket") end" — [Game data](/world/game-data/)
> "player:give("stone_pickaxe") -- one; canonical item name; errors on a name this game version lacks" — [Players](/players/player-lifecycle/)
> "player:give{ item = "arrow", count = 16 }" — [Players](/players/player-lifecycle/)
> "player:give{ item = "player_head", skin = "Notch" }" — [Items](/players/inventory/)
