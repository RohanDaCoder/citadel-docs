---
title: "players.on_slot"
description: "Calls fn when a player picks a hotbar slot, 1..9."
---

Part of [`players`](/ref/Players/).

```luau
players.on_slot(fn: (player: Player, slot: number) -> ()) → Connection
```

Calls `fn` when a player picks a hotbar slot, 1..9.

## Parameters

| Name | Type                                     | Required |
| ---- | ---------------------------------------- | -------- |
| `fn` | `(player: Player , slot: number ) -> ()` | yes      |

## Returns

- [`Connection`](/ref/Connection/)

## Used in

> "players.on_slot(function(player, slot) end) -> connection -- hotbar 1..9" — [Input](/players/movement/)
> "- Selecting a slot fires `players.on_slot`." — [Hotbar menus](/ui/menus/)
