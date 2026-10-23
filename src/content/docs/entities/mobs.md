---
title: 'Mobs and spawning'
description: 'Putting mobs in the world with world.spawn, how a mob acts on its own on both kinds of server, the per-kind spawn tri-state, and what mobs drop.'
---

:::note[In short]
A mob acts on its own on both kinds of server, lite included.
`world.spawn(name, pos)` puts a mob — or a kind your pack defined — at a
point and hands back the same handle every entity gets. Whether a kind
spawns by itself is the per-kind `spawn` value; what it leaves behind is
`drop` (or your own `drops` list). An NPC is not a mob: it does not survive
a reload.
:::

## What a mob is

A kind is a **mob** when the game gives it health and a mind of its own: a
cow, a zombie. An arrow, an item and a boat are not mobs. A player is not an
entity here: players are in `players`, never in `world.entities`.

- `game.entities.cow` and `game.entities.Cow` are the same kind; a kind that this game does not have is `nil`.
- `world.entities { mob = true }` lists the mobs only; `{ mob = false }` the rest. The facts of each kind — `max_health`, `width`, `height`, `speed`, `drop`, `hostile` — are on [Game data](/world/game-data/).

## Spawning with world.spawn

`world.spawn(def, pos, data?)` puts an entity at a point and returns its
handle:

```luau
local cow = world.spawn("cow", vec3(8.5, 66, 8.5))    -- the game's own entity
local it = world.spawn(rocket, vec3(8.5, 66, 8.5), { fuse = 40 })  -- a pack kind, with its data
```

- A mob kind of the game by name (`world.spawn("cow", pos)`) is the game's own entity, and takes no `data`.
- A pack's own kind takes the data it starts life holding.
- `nil` for a kind nothing defined and this game does not have.
- `world.on_entity_spawn` tells after a mob appeared, with its handle and name; a natural spawn fires it on every game version that has one, and a pack's own `world.spawn("cow", pos)` fires it too. Mob kinds only.

:::caution[Gotcha]
a0.1.0 spawns nothing on its own. On an Alpha world every
entity in `world.entities { mob = true }` comes from a dungeon spawner,
`/summon` or this call.
:::

## A mob acts on its own

A mob needs no pack code to live its life, whatever the server runs:

- A mob acts on its own on both kinds of server, lite included.
- Each read gets the entity's current state. Check `alive`.
- A mob a pack spawns stays when the script reloads. An NPC does not — see [NPCs](/entities/npcs/).

## The same handle

A mob has the **same handle** as every entity the world moves: `cow.velocity`,
`cow:push(v)` and `cow:nearby(8)` work too. `tostring(cow)` is
`entity(cow, 7)`: the kind's name and the id. The full handle API — position
and rotation, velocity and push, intent fields, `e.data`, queries — is
[Entity handles](/entities/entity-handles/).

## Natural spawning: the spawn value

`spawn` is the field of a mob kind that a pack writes. It says whether the
kind is in this world by itself:

| Value | Meaning |
| --- | --- |
| `true` | The kind is in this world as the game defines it. It spawns by the game's own rule, and it is the game's entity in full. |
| `false` | The kind never spawns by itself. |
| `nil` | The pack sets nothing. The world's default applies. |

- The world's default is off on a `mode: lite` world and in a room made by `rooms.create`: no mob spawns by itself. The default is on on a `mode: full` world and after `world.rules{ survival = true }`.
- `false` stops natural spawning only. A spawner block, `world.spawn`, `/summon` and breeding still make the entity. Mobs already in the world stay.
- The value is for one room and one pack. `game` is the main room's table; a room from `rooms.create` has its own: `room.game.entities.cow.spawn = true`. If one pack sets `false`, the kind does not spawn.
- On a game with no natural spawning, every write is an error, `nil` included. a0.1.0 to a0.1.3 are such games.
- `true` makes the kind the game's entity in full, on a lite world too: its hits hurt players and a player's right click has the game's effect, unless a pack sets `attacks` or `interact`.

The full rules — per-world defaults, the `attacks`/`interact` fields and how
`nil` resolves against the room's rules — are in
[Game data](/world/game-data/).

## Drops

What a death leaves behind is a fact of the kind, read from `game.entities`,
or a list your pack writes on its own kinds:

- `game.entities.cow.drop` reads the item a mob kind's death leaves behind — `"leather"` for a cow; `nil` for none.
- A pack-defined living body lists its own `drops`: rows of `{ item = "stick", count = 2 }`, `count = { 1, 3 }` for a random count, `chance = 0.05` for a row that comes from one death in twenty. See [Custom entities](/entities/custom-entities/).
- A game **block's** `drops` — whether a block leaves its item when the world breaks it by itself — is a separate `true`/`false`/`nil` field of a game block, also in [Game data](/world/game-data/).
- `world.on_entity_death` tells after a mob died; it is gone, so its id and name is all there is. Mob kinds only.

## See also

- [Custom entities](/entities/custom-entities/) — `game.entities.define` in full: the living body, its `drops`, and amending mob behaviour.
- [Entity handles](/entities/entity-handles/) — the handle a mob hands you: `velocity`, `:push`, `:nearby`, `alive`.
- [Game data](/world/game-data/) — the `spawn`, `attacks` and `interact` tri-states in full; a kind's facts.
- [NPCs](/entities/npcs/) — the player-shaped entity that does not survive a reload.
- [World state](/world/world-state/) — `world.rules`: the `survival` and `damage` rules behind the spawn defaults.
