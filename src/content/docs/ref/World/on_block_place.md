---
title: "world.on_block_place"
description: "Tells after a block was placed, with its canonical name"
---

Part of [`world`](/ref/World/).

```luau
world.on_block_place(fn: (player: Player ?, pos: Vec3, block: string) -> ()) → Connection
```

Tells after a block was placed, with its canonical name. Observe-only; `player` is nil when nobody placed it or they left.

## Parameters

| Name | Type                                                   | Required |
| ---- | ------------------------------------------------------ | -------- |
| `fn` | `(player: Player ?, pos: Vec3 , block: string ) -> ()` | yes      |

## Returns

- [`Connection`](/ref/Connection/)

## Used in

> "world.on_block_place(function(player, pos, block) end) -> connection" — [Game events](/concepts/events/)
> "`world.on_block_break` or `world.on_block_place`." — [Cancelling events](/concepts/events/)
