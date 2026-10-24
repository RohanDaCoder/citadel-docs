---
title: "players.on_damage"
description: "Asks fn before damage lands on a player; return false to refuse it"
---

Part of [`players`](/ref/Players/).

```luau
players.on_damage(fn: (player: Player ?, hit: DamageHit) -> boolean ?) → Connection
```

Asks `fn` before damage lands on a player; return false to refuse it. A missed deadline denies it. A pack's own `player:damage` is not asked about.

## Parameters

| Name | Type                                             | Required |
| ---- | ------------------------------------------------ | -------- |
| `fn` | `(player: Player ?, hit: DamageHit ) -> boolean` | no       |

## Returns

- [`Connection`](/ref/Connection/)

## Used in

> "players.on_damage(function(player, hit) return false end) -> connection" — [Cancelling events](/concepts/events/)
> "players.on_damage(function(player, hit)" — [Cancelling events](/concepts/events/)
> "`players.on_damage` (kind `"damage"`). With no answer in time, the engine" — [Limits and reload](/systems/limits/)
