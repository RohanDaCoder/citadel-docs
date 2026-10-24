---
title: "players.on_join"
description: "Calls fn when a player arrives: on the globals when a client connects, on a room's table each time a player moves into it."
---

Part of [`players`](/ref/Players/).

```luau
players.on_join(fn: (player: Player) -> ()) → Connection
```

Calls `fn` when a player arrives: on the globals when a client connects, on a room's table each time a player moves into it.

## Parameters

| Name | Type                      | Required |
| ---- | ------------------------- | -------- |
| `fn` | `(player: Player ) -> ()` | yes      |

## Returns

- [`Connection`](/ref/Connection/)

## Used in

> "players.on_join(function(player)" — [Guide: Your first pack](/getting-started/quick-start/)
> "`players.on_join` registers another function, this time for a player joining." — [Guide: Your first pack](/getting-started/quick-start/)
> "players.on_join(function(player)" — [Guide: Coin rush](/guides/guide-coin-rush/)
> "players.on_join(function(player)" — [Guide: Coin rush](/guides/guide-coin-rush/)
> "players.on_join(function(player)" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
> "room.players.on_join(function(p)" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
