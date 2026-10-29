---
title: 'Health and damage'
description: 'player.health, max_health, food and saturation — nil where the game version has no rule, the 1..1024 maximum, healing and respawn — plus player:damage, the death causes, the damage/fall/survival room rules and PvP through players.on_click.'
---

:::note[In short]
`player.health`, `max_health`, `food` and `saturation` are
`nil`, not `0`, on a game version with no rule for them. The maximum is 1
to 1024, lasts for the session and every Java client draws its hearts. On a
pack server only `damage` and `health` hurt a player; PvP is the pack's job
through `hit.player` in `players.on_click`, and `world.rules` switches the
engine's own damage on.
:::

## nil, not zero

`player.health`, `player.max_health`, `player.food` and `player.saturation`
are `nil`, not `0`, on a game version with no rule for them. Every Alpha node
is one (a0.1.0 has no food and no damage). Across the engine, what a version
lacks is absent, not zero.

`health` is always the health of one individual now. `max_health` is always
the most it can be. This is the same for a player, for an entity in the world
and for a kind (a kind has `max_health` only).

## The maximum: `max_health`

| Write                                        | Result                              |
| -------------------------------------------- | ----------------------------------- |
| `player.max_health = n` (1 to 1024)          | Sets the most health they can have. |
| `player.max_health = nil`                    | Gives the game's own (20) back.     |
| Another type, or out of range                | An error.                           |
| Any write, on a version with no damage rules | An error.                           |

- A lower maximum takes `player.health` down to it. A higher maximum does not
  heal.
- The maximum lasts for the session, also across rooms and deaths. Set it in
  `players.on_join`.
- Every Java client (1.7 to 26.3) draws the hearts of the maximum. A Bedrock
  client draws no health today.

## health, food and saturation

| Field               | Meaning                                                                                |
| ------------------- | -------------------------------------------------------------------------------------- |
| `player.health`     | Their health now, 0 to `max_health`; `nil` where the game version has no damage rules. |
| `player.max_health` | The most health they can have: 20 unless a pack set it.                                |
| `player.food`       | 0..20, or nil where the game version has no food bar.                                  |
| `player.saturation` | The food saturation, or nil where the game version has no food bar.                    |
| `player.dead`       | True while the player is on the death screen.                                          |

`player.health` is writable: set outright, no flash; `0` is a death; a number
above `max_health` stops there. Food, regeneration and peaceful healing stop
at the maximum. A respawn fills to it.

## Hurting a player

- On a pack server, only `damage` and `health` hurt a player. Creative and
  spectator players take no damage.
- [`player:damage(amount)`](/ref/Player/damage/) is a hit in half-hearts: the
  flash, the sound, the resistance window. It returns `false` on a version
  with no damage rules.
- [`player:kill()`](/ref/Player/kill/) kills the player; it returns `false` on
  a version with no damage rules.
- At zero health the player dies. `players.on_death` fires with cause
  `"other"` (a pack's own `player:damage`), and the client shows the respawn
  screen.
- On a pack server a death drops and clears nothing. The hotbar is a menu,
  not an inventory.

:::note
A pack's own `player:damage` call is not asked about —
`players.on_damage` never sees it, in this pack or another. Damage the
engine itself deals is asked first: `false` refuses it, `hit` carries the
amount, cause, attacker and mob kind. The ask model, its two-millisecond
deadline and the `hit` fields are in [The event model](/concepts/events/).
:::

## Death and respawn events

`players.on_death` receives the player (nil once they have left), the cause,
the broadcast English death line as `message`, and `by` — the player who hit
or shot them, or `nil`:

| `cause`                                                                  | What it is                    |
| ------------------------------------------------------------------------ | ----------------------------- |
| `fall`, `drown`, `suffocate`, `void`, `lava`, `fire`, `cactus`, `starve` | The environment.              |
| `attack`                                                                 | A mob's or a player's hit.    |
| `shot`                                                                   | An arrow.                     |
| `blast`, `magic`                                                         | An explosion, magic.          |
| `other`                                                                  | A pack's own `player:damage`. |

`players.on_respawn` fires when they come back; a respawn fills health to the
maximum. The session facts — one player value, `data` kept ten seconds — are
in [Player lifecycle](/players/player-lifecycle/).

## Room rules: damage, fall, survival

A `mode: full` server has them all on; a pack can turn one off. The
`world.rules` facts in full are on [World state](/world/world-state/) — what
matters for health:

- A rule is `true` or `false`. A rule left out keeps its value, and so does a
  rule written as `nil`. Any other value is an error:
  `world.rules{ fall = 0 }` and `world.rules{ fall = "off" }` stop the script.
- `survival` gives the room to the engine's survival, as on a `mode: full`
  server: it turns on `fall`, `damage`, `hunger`, `anticheat` and
  `day_cycle`; a death drops the inventory, and the respawn button works.
- Anticheat checks each Java client's claims: a hit on something the player
  does not look at, or faster than 20 per second, does not land; a claim to
  stand on nothing does not prevent fall damage.

Anything that is not a rule is the pack's job: `player:damage` for a hit,
`player.health` to heal, `players.on_death` and `players.on_respawn` for what
happens next, and `hit.player` in `players.on_click` for one player hitting
another:

```luau
world.rules{ fall = true }
players.on_click(function(player, hit)
    if hit.button == "left" and hit.player then
        hit.player:damage(2)
        hit.player:push(player:look() * 0.5 + vec3(0, 0.3, 0))
    end
end)
```

## See also

- [Player lifecycle](/players/player-lifecycle/) — join, leave, death and respawn delivery.
- [World state](/world/world-state/) — every `world.rules` entry.
- [The event model](/concepts/events/) — the `on_damage` ask and its deadline.
- [Movement and cameras](/players/movement/) — `push` and the anticheat rule.
- [Inventory](/players/inventory/) — what a survival death drops.
