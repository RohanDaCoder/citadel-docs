---
title: 'players.on_death'
description: 'Calls fn when a player dies, with the cause (fall, drown, void, lava, ...) and the line broadcast; player is nil once they have left.'
---

Part of [`players`](/ref/Players/).

```luau
players.on_death(fn: (player: Player ?, cause: string, message: string, by: Player ?) -> ()) → Connection
```

Calls `fn` when a player dies, with the cause (fall, drown, void, lava, ...) and the line broadcast; `player` is nil once they have left.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `fn` | `(player: Player ?, cause: string , message: string , by: Player ?) -> ()` | yes |

## Returns

- [`Connection`](/ref/Connection/)

## Used in

> "players.on_death(function(player, cause, message, by) end) -> connection   -- by: the player who did it, or nil" — [Players](/players/player-lifecycle/)
> "`cause` in `players.on_death` is one of `fall`, `drown`, `suffocate`, `void`," — [Players](/players/player-lifecycle/)
> "- At zero health the player dies. `players.on_death` fires with cause" — [Body and movement](/players/movement/)
> "`player.health` to heal, `players.on_death` and `players.on_respawn` for what" — [Room rules](/world/world-state/)
