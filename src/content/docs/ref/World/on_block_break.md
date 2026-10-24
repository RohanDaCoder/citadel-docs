---
title: 'world.on_block_break'
description: 'What the survival tick did'
---

Part of [`world`](/ref/World/).

```luau
world.on_block_break(fn: (player: Player ?, pos: Vec3, block: string) -> ()) → Connection
```

What the survival tick did. Observe-only: the world has already changed, and what the callback returns is not read.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `fn` | `(player: Player ?, pos: Vec3 , block: string ) -> ()` | yes |

## Returns

- [`Connection`](/ref/Connection/)

## Used in

> "world.on_block_break(function(player, pos, block) end) -> connection" — [Game events](/concepts/events/)
> "world.on_block_break(function(player, pos, block)" — [Game events](/concepts/events/)
> "`world.on_block_break` or `world.on_block_place`." — [Cancelling events](/concepts/events/)
> "(`world.on_block_break` and the rest)." — [Limits and reload](/systems/limits/)
