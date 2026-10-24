---
title: 'players.on_drop'
description: 'Calls fn when a stack lands on the ground; player is nil where the world dropped it or they have left.'
---

Part of [`players`](/ref/Players/).

```luau
players.on_drop(fn: (player: Player ?, item: string, count: number) -> ()) → Connection
```

Calls `fn` when a stack lands on the ground; `player` is nil where the world dropped it or they have left.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `fn` | `(player: Player ?, item: string , count: number ) -> ()` | yes |

## Returns

- [`Connection`](/ref/Connection/)

## Used in

> "players.on_drop(function(player, item, count) end) -> connection" — [Game events](/concepts/events/)
