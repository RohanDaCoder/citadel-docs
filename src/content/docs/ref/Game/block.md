---
title: "game.block"
description: "Returns one block in this version's numbers, or nil for a name this game has no word for."
---

Part of [`game`](/ref/Game/).

```luau
game.block(name: string) → Block ?
```

Returns one block in this version's numbers, or nil for a name this game has no word for.

## Parameters

| Name   | Type     | Required |
| ------ | -------- | -------- |
| `name` | `string` | yes      |

## Returns

- [`Block`](/ref/Block/)

## Used in

> "- Queries (`game.block(name)`, the block an entity stands on) return `nil` for" — [API basics](/concepts/conventions/)
> "`game.block(name)` returns one block in **this version's** numbers, or `nil`" — [Game data](/world/game-data/)
> "local stone = game.block("stone")" — [Game data](/world/game-data/)
> "itself leaves no item. `game.block(name).drops = true` switches one block of" — [Room rules](/world/world-state/)
