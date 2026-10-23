---
title: 'game.item'
description: 'Returns an item this game has, or nil for a name it does not; never an error.'
---

Part of [`game`](/ref/Game/).

```luau
game.item(name: string) → Item ?
```

Returns an item this game has, or nil for a name it does not; never an error.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `name` | `string` | yes |

## Returns

- [`Item`](/ref/Item/)

## Used in

> "`game.item(name)` does the same for items: the item's table, or `nil`. It" — [Game data](/world/game-data/)
> "if game.item("bucket") then player:give("bucket") end" — [Game data](/world/game-data/)
