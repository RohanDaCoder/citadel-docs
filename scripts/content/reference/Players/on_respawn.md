---
title: "players.on_respawn"
url: /docs/citadel/reference/Players/on_respawn
---

# players.on_respawn

Calls `fn` when a player respawns; `player` is nil once they have left.

```
players.on_respawn(fn: (player: Player?) -> ()) → Connection
```


## Parameters


## Returns


## Used in
- [`players.on_respawn(function(player) end) -> connection`Players](/docs/citadel/players)
- [``player.health` to heal, `players.on_death` and `players.on_respawn` for what`Room rules](/docs/citadel/room-rules)
