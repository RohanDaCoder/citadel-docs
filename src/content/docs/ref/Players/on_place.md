---
title: 'players.on_place'
description: 'Asks fn before a player puts a block down; return false to cancel it'
---

Part of [`players`](/ref/Players/).

```luau
players.on_place(fn: (player: Player ?, pos: Vec3, block: string) -> boolean ?) → Connection
```

Asks `fn` before a player puts a block down; return false to cancel it. A missed deadline denies the place.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `fn` | `(player: Player ?, pos: Vec3 , block: string ) -> boolean` | no |

## Returns

- [`Connection`](/ref/Connection/)

## Used in

> "Placing it fires `players.on_place`, then the block's `on_place` with the" — [Custom blocks](/world/custom-blocks/)
> "`players.on_break` and `players.on_place` run **before** the world changes. A" — [Cancelling events](/concepts/events/)
> "players.on_place(function(player, pos, block) return false end) -> connection" — [Cancelling events](/concepts/events/)
> "(kind `"break"`), `players.on_place` (kind `"place"`) and" — [Limits and reload](/systems/limits/)
