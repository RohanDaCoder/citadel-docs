---
title: "players.on_leave"
description: "The same player value on_join had; it can no longer be sent to."
---

Part of [`players`](/ref/Players/).

```luau
players.on_leave(fn: (player: Player) -> ()) → Connection
```

The same player value on_join had; it can no longer be sent to.

## Parameters

| Name | Type                      | Required |
| ---- | ------------------------- | -------- |
| `fn` | `(player: Player ) -> ()` | yes      |

## Returns

- [`Connection`](/ref/Connection/)

## Used in

> "room.players.on_leave(function()" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
> "room.players.on_leave(function()" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
> "players.on_leave(function()" — [Scoreboard with a button](/guides/guide-scoreboard-with-a-button/)
> "mine.players.on_leave(function()" — [A world per player](/concepts/rooms-and-dimensions/)
> "players.on_leave(function(player) end) -> connection -- the same player value; it can no longer be sent to" — [Players](/players/player-lifecycle/)
> "room.players.on_leave(function(p) p.visible = true end)" — [Players](/players/player-lifecycle/)
