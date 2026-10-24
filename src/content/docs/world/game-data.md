---
title: "Game data"
description: "The game registry a pack reads — game.block(name) and its fields, the block drops switch, game.item, entity kinds with their facts, the spawn/attacks/interact tri-state fields and their resolution rules, and game.terrain."
---

:::note[In short]
`game` reads the game version a room runs: one block in this
version's numbers with `game.block(name)`, items with `game.item(name)`,
entity kinds with `game.entities.<kind>`, and the overworld's terrain list
with `game.terrain`. The one field a pack writes on the game's own things is
the tri-state `spawn`, `attacks`, `interact` and block `drops` — `true`,
`false` or `nil`.
:::

## `game.block(name)`

[`game.block(name)`](/ref/Game/block/) returns one block in **this version's**
numbers, or `nil` if this game lacks it.

| Field          | Type                                       | Meaning                                                                                                                        |
| -------------- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| `name`         | `string`                                   | The block's canonical name                                                                                                     |
| `behaviour`    | `string?`                                  | The rule Citadel runs for it: `"grass"`, `"flowing"`, `"torch"` or `"falling"`; `nil` for a block that does nothing on its own |
| `hardness`     | `number`                                   | Seconds-scale hardness in this version's numbers; below zero is unbreakable                                                    |
| `random_ticks` | `boolean`                                  | Whether the random-tick pass acts on it                                                                                        |
| `opaque`       | `boolean`                                  | Whether it is an opaque full cube, which is not the material's question                                                        |
| `light`        | `number`                                   | What it gives off, 0..15, and what a step through it takes away                                                                |
| `light_filter` | `number`                                   | What a step through it takes off the light, 0 to 15                                                                            |
| `resistance`   | `number?`                                  | The three the block-update tables own: `nil` in a game that has none                                                           |
| `flammability` | `{ catches: number, burns_away: number }?` | Fire's two numbers: how readily it catches and how fast it burns away                                                          |
| `material`     | `Material?`                                | The jar's Material as five questions; `nil` in a game with no block-update tables                                              |
| `drops`        | `boolean?`                                 | The one field a pack writes — see below                                                                                        |

`resistance`, `flammability` and `material` are `nil`, not zero, in a game with
no block-update tables. Everything above is read-only.

### `drops` — `true`, `false` and `nil`

`drops` is the field of a game block that a pack writes. It says whether a
block of this kind leaves its item when the world breaks it by itself: a torch
whose wall is gone, a leaf that decays, a block an explosion or a piston
breaks, sand that cannot land. On a `mode: lite` world, the world leaves no
such item. The pack switches a block on:

| Value   | Meaning                                                          |
| ------- | ---------------------------------------------------------------- |
| `true`  | The world leaves the block's normal drops, on a lite world too.  |
| `false` | The world leaves nothing for this block, with `survival` on too. |
| `nil`   | The pack sets nothing. The world's default applies.              |

- The world's default is off on a `mode: lite` world and in a room made by
  `rooms.create`. It is on on a `mode: full` world and after
  `world.rules{ survival = true }`.
- The value is for every state of the block, and for this block name only.
  `oak_planks` and `spruce_planks` are two blocks.
- It reads what this pack set, not another pack's value. Where two packs
  disagree, `false` wins.
- It is not a player's dig. Without `survival`, a dig reaches no block.
- Use it for the game's blocks. A block from `game.blocks.define` leaves the
  drops its definition lists.
- A reload removes a value that the script does not set again.
- `true` is an error in a game version with no items on the ground.

## `game.item(name)`

[`game.item(name)`](/ref/Game/item/) does the same for items: the item's table,
or `nil`. It never raises an error.

## Entity kinds

A kind is a `mob` when the game gives it health and a mind of its own: a cow, a
zombie. An arrow, an item and a boat are not mobs. A player is not an entity
here: players are in `players`, never in `world.entities`.

`game.entities.<kind>` has the facts of one kind of the game.
`game.entities.cow` and `game.entities.Cow` are the same kind. A kind that this
game does not have is `nil`: `if game.entities.creeper then`.

```luau
local cow = game.entities.cow
print(cow.max_health, cow.width, cow.height, cow.speed)   -- cow.health is an error: a kind has a maximum
print(cow.drop)                      -- "leather"
print(cow.hostile)                   -- false
print(cow.registry_name)             -- "Cow", this version's own spelling
print(cow.mob)                    -- true: a cow is a mob

for name, kind in game.entities do   -- every mob kind this version has, in its own order
    if kind.hostile then print(name) end
end

local arrow = game.entities.arrow    -- a kind that is not a mob has a row too
print(arrow.mob)                  -- false
print(arrow.width, arrow.height, arrow.physics)

game.entities.names()                    -- every kind: the pack's own and the game's, mob or not
game.entities.names { mob = true }    -- the mob kinds only
game.entities.names { mob = false }   -- the kinds that are not mobs
```

| Fact              | Meaning                                                                                                                                |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `name`            | Its modern registry name: `"cow"`                                                                                                      |
| `mob`             | Whether the kind is a mob: `true` for a cow, `false` for an arrow                                                                      |
| `max_health`      | The most health one of this kind has, in this version's numbers. `health` on a kind is an error: health is what one entity has now     |
| `width`, `height` | Its size in blocks, in this version's numbers                                                                                          |
| `speed`           | Blocks a tick at a full walk                                                                                                           |
| `hostile`         | Whether it is hostile                                                                                                                  |
| `drop`            | The item its death leaves behind, such as `"leather"`; `nil` for none                                                                  |
| `registry_name`   | This version's own registry spelling: `"Cow"`. A dungeon spawner stores this one                                                       |
| `physics`         | For a kind that is not a mob, which order of operations moves it: `"item"`, `"falling"`, `"vehicle"` or `"none"`. `nil` for a mob kind |
| `behaviour`       | The name of the behaviour the engine runs for this kind, such as `"sheep"` or `"living"`                                               |
| `profile`         | Read-only copy; `nil` for a specialized behaviour without a shared profile                                                             |

- Use `for name, kind in game.entities do`, not `pairs(game.entities)`.
- A game kind that is not a mob (an arrow, a boat, primed TNT) has the facts
  `name`, `mob` (`false`), `width`, `height` and `physics`. Every other fact is
  `nil`. A write to `spawn`, `attacks` or `interact` is an error, and so is
  `:amend`: they are for mob kinds.
- Iteration and `game.entities.names()` cover all kinds, once each. Use
  `game.entities.names { mob = true }` or check `kind.mob` for mob settings.
- A pack kind (`rave:rocket`) reads as a definition handle, with `name` and
  `mob = false`. Pass it to `world.spawn` just like the handle from `define`.
- `define`, `amend` and `names` are functions on the same table (see
  [Custom entities](/entities/custom-entities/)). `game.entities.cow:amend { ... }`
  is the same as `game.entities.amend("cow", { ... })`.

Everything above is read-only.

## `spawn` — `true`, `false` and `nil`

`spawn` is the field of a mob kind that a pack writes. It says whether the kind
is in this world by itself. On a `mode: lite` world, no mob spawns by itself;
the pack switches a kind on, and it then spawns by the game's own rule.

| Value   | Meaning                                                                                                                  |
| ------- | ------------------------------------------------------------------------------------------------------------------------ |
| `true`  | The kind is in this world as the game defines it. It spawns by the game's own rule, and it is the game's entity in full. |
| `false` | The kind never spawns by itself.                                                                                         |
| `nil`   | The pack sets nothing. The world's default applies.                                                                      |

- The world's default is off on a `mode: lite` world and in a room made by
  `rooms.create`: no mob spawns by itself. The default is on on a `mode: full`
  world and after `world.rules{ survival = true }`: each kind spawns by the
  game's own rule. `world.rules{ survival = false }` sets the default to off
  again.
- `true` makes the kind the game's entity in full, on a lite world too. It
  spawns by the game's own rule. Its hits hurt players and a player's right
  click on it has the game's effect. See
  [`attacks` and `interact`](#attacks-and-interact).
- A monster that comes to a sleeping player obeys the same value.
- `true` does not make a kind spawn where the game cannot spawn it. On 1.8.9
  the game takes the kinds it spawns from the biome. A world with no biomes (a
  world the scripts make) spawns nothing, and `true` is an error there.
- `false` stops natural spawning only. A spawner block, `world.spawn`,
  `/summon` and breeding still make the entity.
- Mobs already in the world stay.
- Reading gives what this pack set: `true`, `false` or `nil`. It does not give
  the game's own rule or the value of a different pack.
- Each pack has its own value. If one pack sets `false`, the kind does not
  spawn. If no pack sets `false` and one pack sets `true`, the kind is on.
- The value is for one room. `game` is the main room's table. A room from
  `rooms.create` has its own: `room.game.entities.cow.spawn = true`.
- On a script reload, the values of the last run stay until the new script has
  loaded. Then each value that the new script did not set is removed.
- On a game with no natural spawning, every write is an error, `nil` included.
  a0.1.0 to a0.1.3 are such games.
- An error is a plain string for `pcall`.

## `attacks` and `interact`

`attacks` and `interact` are two more fields of a mob kind that a pack writes.
Each is `true`, `false` or `nil`. A different value is an error.

| Field      | `true`                                                                                           | `false`                                |
| ---------- | ------------------------------------------------------------------------------------------------ | -------------------------------------- |
| `attacks`  | The entity's hits hurt players.                                                                  | The entity's hits do not hurt players. |
| `interact` | A player's right click on the entity has the game's effect (milk from a cow, a saddle on a pig). | The right click has no effect.         |

With `nil`, the engine uses the first line that applies:

1. The kind has `spawn = true`: the field is on.
2. The room's rule: `damage` for `attacks`, `survival` for `interact`.

- **The kind's own setting is stronger than the room's rule.** Thus
  `game.entities.zombie.spawn = true` makes a zombie's hit hurt in a room with
  `world.rules{ damage = false }`. To keep the zombie harmless there, set
  `game.entities.zombie.attacks = false`.
- A zombie from `world.spawn` on a lite world does not hurt players until the
  pack sets `spawn = true` or `attacks = true` for zombies, or the room has the
  `damage` rule.
- `interact` changes the item in the player's hand as the game does: an empty
  bucket becomes a bucket of milk.
- `interact` is not available on 1.8.9: that game version has no right click on
  a mob in Citadel. `interact = true` is an error there, and `spawn = true`
  does not give the right click.
- `attacks` covers the entity's own hit, its arrow and its blast. An arrow
  keeps the kind of its shooter, so the arrow of a dead skeleton follows
  `game.entities.skeleton.attacks`. The blast of a creeper follows
  `game.entities.creeper.attacks`.
- `attacks = false` stops the damage to players only. The blast of a creeper
  still breaks blocks, as the game says, and still hurts other entities.
- A blast of TNT, of a bed and of `world.explode` has no kind. It follows the
  room's `damage` rule.
- The fields are for one room and one pack, as `spawn` is. If one pack sets
  `false`, the field is off.

To put mobs in a world, use [`world.spawn(name, pos)`](/ref/World/spawn/) (see
[Mobs](/entities/mobs/)), `/summon`, or a dungeon spawner the terrain placed.

:::note
a0.1.0 spawns nothing on its own. Only its dungeon spawner makes
mobs.
:::

## `game.terrain`

[`game.terrain`](/ref/Game/terrain/) describes this world's overworld: `snow`,
and `steps` in the shape citadel.yml uses. It is read-only, and `nil` where the
engine has no list.

```luau
for i, step in ipairs(game.terrain.steps) do
  print(i, step.step, step.block, step.count)   -- 1 dungeons nil 8
end
print(game.terrain.snow)                        -- false
```

The step names and their keys are in
[Terrain generation](/world/terrain-generation/#the-a010-terrain-steps).

## See also

- [Terrain generation](/world/terrain-generation/) — the terrain steps the
  overworld runs, and where `game.terrain` comes from.
- [World state](/world/world-state/) — the `survival` and `damage` rules that
  `drops`, `spawn`, `attacks` and `interact` resolve against.
- [Custom entities](/entities/custom-entities/) — `game.entities.define` and `amend`
  for kinds of your own.
- [Mobs](/entities/mobs/) — `world.spawn` and what mobs drop.
- [Rooms and dimensions](/concepts/rooms-and-dimensions/) — per-room `game` tables.
