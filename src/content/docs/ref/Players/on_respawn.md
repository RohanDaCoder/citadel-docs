---
title: 'players.on_respawn'
description: 'Calls fn when a player respawns; player is nil once they have left.'
---

Part of [`players`](/ref/Players/).

```luau
players.on_respawn(fn: (player: Player ?) -> ()) → Connection
```

Calls `fn` when a player respawns; `player` is nil once they have left.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `fn` | `(player: Player ?) -> ()` | yes |

## Returns

- [`Connection`](/ref/Connection/)

## Used in

> "players.on_respawn(function(player) end) -> connection" — [Players](/players/player-lifecycle/)
> "`player.health` to heal, `players.on_death` and `players.on_respawn` for what" — [Room rules](/world/world-state/)
