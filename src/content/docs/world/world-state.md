---
title: 'World state'
description: 'The room-level switches and clocks — world.rules with its seven boolean rules and read/write semantics, the time of day with world.time, weather, world.explode, and where players arrive with world.spawn_point.'
---

:::note[In short]
the switches a pack flips on a room and the clocks it reads.
`world.rules` turns the parts of the player simulation on and off —
survival, fall, damage, hunger, anticheat, day_cycle and redstone — with
strict boolean semantics. `world.time` holds or drives the sky, and
`world.explode` and `world.spawn_point` finish the room-level world calls.
:::

## `world.rules`

```luau
world.rules(opts: { survival: boolean?, fall: boolean?, damage: boolean?,
                    hunger: boolean?, anticheat: boolean?, day_cycle: boolean?,
                    redstone: boolean? }?) -> Rules
```

[`world.rules{ fall = true }`](/ref/World/rules/) switches one on, `false` off.
A rule left out or `nil` keeps its value, and **a number or a string is an
error**: `world.rules{ fall = 0 }` and `world.rules{ fall = "off" }` stop the
script. [`world.rules()`](/ref/World/rules/) with no argument reads them.

| Rule | What it runs |
| --- | --- |
| `survival` | the engine's survival — and it turns `fall`, `damage`, `hunger`, `anticheat` and `day_cycle` on |
| `fall` | fall damage |
| `damage` | hits and blasts hurt players |
| `hunger` | the food bar |
| `anticheat` | the movement and hit checks |
| `day_cycle` | the sun moves |
| `redstone` | signals move in the room |

A `mode: full` server has them all on; a pack can turn one off. On a pack
server they are all off until the pack says — except `anticheat` and `redstone`,
which are on everywhere until a pack turns them off.

### `survival`

`survival` gives the room to the engine's survival, as on a `mode: full`
server:

- A broken block drops its normal drops.
- A block the world breaks by itself drops them too: a torch whose wall is
  gone, a leaf that decays, a block an explosion or a piston breaks, sand that
  cannot land.
- Placing uses up the stack.
- The inventory and a crafting table craft.
- A death drops the inventory, and the respawn button works.
- The engine saves the player's inventory.
- It also turns on `fall`, `damage`, `hunger`, `anticheat` and `day_cycle`.

Without `survival`, a dig reaches no block, and a block the world breaks by
itself leaves no item. [`game.block(name).drops = true`](/ref/Block/drops/)
switches one block of the game back on — see [Game data](/world/game-data/). A
pack block still leaves the drops its definition lists; `drops = "table"` is
the game's own drop and leaves nothing.

:::tip
a survival pack puts `world.rules{ survival = true }` at the top, and
runs the same on either kind of server.
:::

### `redstone`

`redstone` is on in every room until a pack turns it off. With it off, no
signal moves: a lever lights no wire, a piston stays in, a pack block's `power`
gives nothing and `block.powered` reads `false`. What was lit when the rule
changed stays as it is until something beside it changes.

### `anticheat`

`anticheat` checks what each Java player's client claims:

- A player who flies, runs too fast, sends moves faster than the game ticks, or
  walks through full blocks goes back to the last legal position.
- A claim to stand on nothing does not prevent fall damage.
- A hit on something the player does not look at, or faster than 20 per second,
  does not land.
- After enough failed checks in a short time, the engine removes the player.
  The message names the check.
- The flight check skips creative and spectator players, a player who may fly
  (`player.can_fly`), a rider and a dead player.
- `player:push` and a movement effect (`speed`, `jump_boost`, `levitation`,
  `slow_falling`, `dolphins_grace`) exempt the player while they last.
  `player:teleport` is always allowed.

:::caution[Gotcha]
a pack that moves players in any other way turns `anticheat` off:
`world.rules{ anticheat = false }`.
:::

### Anything else is the pack's job

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

## The time of day

The time is in ticks, 0 at dawn and 24000 to a day. Each room has its own time,
and late joiners get the same sky.

```luau
world.time("night")          -- sets the hour: sunrise 23000, day 1000, noon 6000, sunset 12000, night 13000, midnight 18000
world.time(18000)            -- sets the hour, in ticks
world.time(function(s)       -- a cycle: asked each tick, s seconds after this call
    return 1000 + s * 40     -- a day of ten minutes, from morning
end)
world.time(function(s)       -- anything the pack likes: a day that stops at dusk
    return math.min(1000 + s * 20, 12000)
end)
local now = world.time()     -- 0 .. 23999
```

- A call replaces the previous one, a function too.
- The function returns ticks or a name. If it errors, the sky stays where it
  was.
- Whether the sun moves is a rule: `world.rules{ day_cycle = true }` runs the
  version's own day (20 minutes), and nothing else of survival.
- On a `mode: lite` world and in a room made by `rooms.create`, the rule is off
  and the sun stays straight overhead (noon).
- On a `mode: full` world, and after `world.rules{ survival = true }`, the rule
  is on.
- A number or a name sets the hour. With `day_cycle` on, the day runs on from
  there, as `/time set` does. With it off, the sky stays there.
- A function drives the sky itself. The engine's day stands aside until the
  next `world.time` call.

:::note
a stopped sky, the normal day or an `s * 20` day costs one packet a
second. A faster or slower day costs one packet every tick it moves.
:::

**Weather** is not a world call: a biome's `weather` field is the weather there
(see [Terrain generation](/world/terrain-generation/#biomes)), and a dimension
turns it off with `type: { weather: false }`. The world's `level.json` keeps
the seed, spawn, time and weather of the first run.

## `world.explode`

```luau
world.explode(pos: Vec3, power: number?)
```

A blast at a point. The power is clamped by this game's own column and the
tick's explosion budget decides when it goes off, never whether. A blast of
`world.explode` has no kind — it follows the room's `damage` rule.

## `world.spawn_point`

[`world.spawn_point`](/ref/World/spawn_point/) is where players arrive in this
room; writable, and the same value as the room's `spawn_point`.

- A write changes where a player arrives: on a join, on a respawn, and on a
  move to the room. The clients in the room get the new compass target.
- The write is **not stored**. After a restart the room has the point of
  `citadel.yml` or of the stored world again.
- The write does not move the chunks that stay loaded, the spawn protection, or
  the area where no mob spawns by itself. Those stay at the first point.

The full treatment, including `player.spawn_point` for a player's own respawn
point, is in [Rooms and dimensions](/concepts/rooms-and-dimensions/#spawn-points-precisely).

## See also

- [Rooms and dimensions](/concepts/rooms-and-dimensions/) — per-room tables, spawn
  points, dimensions.
- [Game data](/world/game-data/) — the `drops`, `spawn`, `attacks` and `interact`
  fields that resolve against these rules.
- [Custom blocks](/world/custom-blocks/) — `block.powered` and pack block power,
  which `redstone` switches off.
- [Terrain generation](/world/terrain-generation/) — biome weather.
- [Health](/players/health/) — what `damage` and `fall` mean for a player.
