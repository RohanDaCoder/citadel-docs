---
title: 'players.on_pickup'
description: 'A stack taken off the ground, and one that landed on it'
---

Part of [`players`](/ref/Players/).

```luau
players.on_pickup(fn: (player: Player ?, item: string, count: number) -> ()) → Connection
```

A stack taken off the ground, and one that landed on it. `player` is nil where the world dropped it, or where they have already left.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `fn` | `(player: Player ?, item: string , count: number ) -> ()` | yes |

## Returns

- [`Connection`](/ref/Connection/)

## Used in

> "players.on_pickup(function(player, item, count) end) -> connection" — [Game events](/concepts/events/)
