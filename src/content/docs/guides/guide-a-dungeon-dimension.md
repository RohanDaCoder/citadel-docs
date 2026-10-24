---
title: 'A dungeon dimension'
description: 'Add a second world to a pack — declare a dungeon dimension in citadel.yml, generate mossy corridors under a bedrock roof, step on a carpet to travel in, and /leave to come back.'
---

:::note[In short]
this tutorial adds a second world to a pack: `dungeon`,
declared in `citadel.yml` and generated in code, with bedrock at both
ends and two crossing corridors a client draws with the Nether's dark
sky. Stepping on a square of carpet routes a player in; `/leave` brings
them back. It is the guide for dimensions and routes.
:::

## What you build
- A castle yard of stone bricks with a square of blue carpet in it.
- `dungeon`, a second world: bedrock at both ends, mossy walls, two
  crossing corridors. A client draws it with the Nether's dark sky.
- Step on the carpet and you arrive in the dungeon. `/leave` brings you
  back.

## Before you start

This guide builds on [Quick start](/getting-started/quick-start/): `world.on_generate`
and `commands.add`. The concept page behind this tutorial is
[Rooms and dimensions](/concepts/rooms-and-dimensions/).

## 1. Declare the dimension

A pack adds a world in `citadel.yml`, under `dimensions:`. The name is its
id inside the pack, so this one is `castle:dungeon`:

```yaml
# citadel.yml
name: castle
entry: main.luau
motd: A castle with a dungeon under it
spawn_point: [0.5, 65.0, 0.5]
gamemode: 2
mode: lite
world: script
dimensions:
  dungeon:
    type: { has_skylight: false, has_ceiling: true, weather: false }
    world: script
```

- `type` says how the world behaves. Every field is optional and starts
  from the main world's: `has_skylight`, `has_ceiling`, `weather`,
  `ultrawarm`, `bed_works`, `respawn_anchor_works`, `coordinate_scale`,
  `fixed_time` and `effects`.
- A world with a roof looks like the Nether to a client, one with no sky
  and no roof like the End. `effects` chooses one of the three yourself.
- `world: script` means the pack makes its chunks. `void` leaves them
  empty.

The dungeon is a world of the server's group: it ticks after the main world
and, on a server that keeps its world, saves to `world_dungeon` beside it.

:::note
the manifest is read once at boot — add the dimension before
the server starts, and restart after any edit to `citadel.yml`
(see [Quick start](/getting-started/quick-start/)).
:::

## 2. The yard

The main world, as in the first guide:

```luau
-- main.luau
-- The castle yard: a stone floor, and a square of blue carpet in the middle.
world.on_generate(function(chunk)
    chunk:fill(vec3(chunk.min.x, 64, chunk.min.z), vec3(chunk.max.x, 64, chunk.max.z), "stone_bricks")
    chunk:fill(vec3(4, 65, 4), vec3(5, 65, 5), "light_blue_carpet")
end)
```

## 3. The dungeon's terrain

`world.dimension(name)` is that world's own `world` table. Its
`on_generate` fills the dungeon's chunks:

```luau
-- main.luau
-- The dungeon: bedrock below and above, dark corridors in between.
local dungeon = world.dimension("dungeon")
dungeon.on_generate(function(chunk)
    chunk:fill(vec3(chunk.min.x, 63, chunk.min.z), vec3(chunk.max.x, 63, chunk.max.z), "bedrock")
    chunk:fill(vec3(chunk.min.x, 64, chunk.min.z), vec3(chunk.max.x, 68, chunk.max.z), "mossy_cobblestone")
    chunk:fill(vec3(chunk.min.x, 64, chunk.min.z + 6), vec3(chunk.max.x, 66, chunk.min.z + 9), "air")
    chunk:fill(vec3(chunk.min.x + 6, 64, chunk.min.z), vec3(chunk.min.x + 9, 66, chunk.max.z), "air")
    chunk:fill(vec3(chunk.min.x, 69, chunk.min.z), vec3(chunk.max.x, 69, chunk.max.z), "bedrock")
end)
```

## 4. The gate

A route is how a player gets from one world to another. This one starts in
the overworld, and the trigger is standing in a block:

```luau
-- main.luau
-- Step on the carpet and you are in the dungeon.
routes.add{
    from = "overworld",
    to = "dungeon",
    trigger = { block = "light_blue_carpet" },
    placement = { x = 7.5, y = 64, z = 7.5 },
}
```

- `trigger = { block = "light_blue_carpet" }` fires on the first tick a
  player stands in carpet. `ticks = 80` would make them wait, as a Nether
  portal does.
- `placement` is where they arrive. Leave it out and they arrive at the
  dungeon's spawn.

:::caution[Gotcha]
after a trip a player must step out of the trigger block for
half a second before it can fire again.
:::

## 5. The way back

`player:travel(dimension, pos)` sends a player to any world of the group, at
`pos` or, without it, at its spawn:

```luau
-- main.luau
-- `/leave` goes back up, to the yard's spawn.
commands.add("leave", function(player)
    player:travel("overworld")
end)
```

## Try it

Run the pack, step on the carpet, look up at the roof, and type `/leave`.

## Where to go next

- [Rooms and dimensions](/concepts/rooms-and-dimensions/) — dimensions, routes
  and `travel` in depth, and rooms, the runtime way to another world.
- [Pack anatomy](/concepts/pack-anatomy/) — the manifest's `dimensions` key and
  every other key.
- [Terrain generation](/world/terrain-generation/) — `on_generate` and the
  chunk API.
- [Commands](/systems/commands/) — typed arguments, help text.
- [Cookbook: teleport pads](/cookbook/cookbook-teleport-pads/) — the
  trigger-block route pattern, alone.

## See also

- [Parkour, a room each](/guides/guide-parkour-a-room-each/) — rooms: a world
  per player, made at runtime.
- [Coin rush](/guides/guide-coin-rush/) — zones, scores, rounds.
- [Build a cottage](/guides/guide-build-a-cottage/) — building well, in code.
