---
title: "players.on_damage"
url: /docs/citadel/reference/Players/on_damage
---

# players.on_damage

Asks `fn` before damage lands on a player; return false to refuse it. A missed deadline denies it. A pack's own `player:damage` is not asked about.

```
players.on_damage(fn: (player: Player?, hit: DamageHit) -> boolean?) → Connection
```


## Parameters


## Returns


## Used in
- [`players.on_damage(function(player, hit) return false end) -> connection`Cancelling events](/docs/citadel/cancelling-events)
- [`players.on_damage(function(player, hit)`Cancelling events](/docs/citadel/cancelling-events)
- [``players.on_damage` (kind `"damage"`). With no answer in time, the engine`Limits and reload](/docs/citadel/limits-and-reload)
