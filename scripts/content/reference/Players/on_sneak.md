---
title: "players.on_sneak"
url: /docs/citadel/reference/Players/on_sneak
---

# players.on_sneak

Calls `fn` once per sneak press and release; `down` is true on the press.

```
players.on_sneak(fn: (player: Player, down: boolean) -> ()) → Connection
```


## Parameters


## Returns


## Used in
- [`players.on_sneak(function(player, down) end) -> connection -- once per press and release`Input](/docs/citadel/input)
- [`- Without `locked`, sneaking gets a rider off and fires `players.on_sneak`.`Displays](/docs/citadel/displays)
