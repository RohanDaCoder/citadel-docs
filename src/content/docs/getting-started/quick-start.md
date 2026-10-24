---
title: 'Quick start'
description: 'Build a first Citadel pack from scratch — manifest, script, terrain, a join handler, a command — then run it, edit it live, and understand what the reload did.'
---

:::note[In short]
a Citadel pack is two files — a `citadel.yml` manifest and one
Luau entry script. This page builds a small lobby pack: generated ground, a
welcome title, and a `/spawn` command. Then it changes one line while the
server is running and watches the hot reload. About five minutes, end to end.
:::

## 1. Create the pack folder

Make a folder named `first` and put this `citadel.yml` inside it:

```yaml
# citadel.yml
name: first
entry: main.luau
motd: My first Citadel pack
spawn_point: [0.5, 65.0, 0.5]
gamemode: 2
mode: lite
world: script
```

What each key did:

| Key | Meaning |
| --- | --- |
| `entry` | The script to run: `main.luau`, beside this file. |
| `world: script` | Your script supplies the terrain through `world.on_generate`. A chunk the script does not fill is air. |
| `mode: lite` | The pack is the game — no survival underneath. |
| `gamemode: 2` | Adventure mode: players explore without breaking the floor. |
| `spawn_point` | Where players arrive: `[0.5, 65.0, 0.5]` puts their feet one block above the floor, centred on the gold marker you create next. |
| `motd` | The message of the day shown in the server list. |

## 2. Add the script

Create `main.luau` beside `citadel.yml`:

```luau
--!strict
-- A small lobby: solid ground, a welcome, and a way back to spawn.

world.on_generate(function(chunk)
    chunk:fill(
        vec3(chunk.min.x, 64, chunk.min.z),
        vec3(chunk.max.x, 64, chunk.max.z),
        "stone"
    )
    chunk:set(vec3(0, 64, 0), "gold_block")
end)

players.on_join(function(player)
    player.ui.title{
        title = "Welcome",
        subtitle = player.name,
        color = "aqua",
    }
    player:message("Walk around, then type /spawn to return to the gold block.", "aqua")
end)

commands.add("spawn", function(player)
    player:teleport(world.spawn_point)
    player:message("You are back at spawn.", "green")
end, { help = "Return to the lobby spawn" })
```

Read the three callbacks in order — they are the three ideas a pack is built
from:

- **`world.on_generate`** fills each chunk with a stone floor at y = 64, then
  marks `(0, 64, 0)` with gold. `chunk:set` ignores positions outside its own
  chunk. `vec3(x, y, z)` describes a position; y is height. A chunk is 16 by
  16 blocks, and the callback must make the **same blocks every time** it runs
  for a position (see [Terrain generation](/world/terrain-generation/)).
- **`players.on_join`** receives the player who joined. The title and the
  message go to that player alone. You register the callback once; Citadel
  calls it when the event happens.
- **`commands.add`** registers `spawn` — the name without the slash. When a
  player types `/spawn`, `player:teleport(world.spawn_point)` returns them to
  the point from the manifest, so the coordinates live in one place.

## 3. Run it

With `citadel` on your `PATH`, run this from the directory containing `first`:

```sh
citadel --lite --pack ./first
```

Join `localhost:25565` from Minecraft Java Edition (any version from 1.8 up).
You should see the welcome title and stand on the gold block. Walk away, type
`/spawn`, and check that you return to it with a confirmation in chat.

If nothing works, read the server log first — a script error in a callback
names the file and line, and a load failure explains which budget was exceeded
(see [The tick budget](/concepts/runtime/#the-tick-budget)).

## 4. Edit it while it runs

Change `title = "Welcome"` to `title = "My lobby"` and save the file. Citadel
reloads `.luau` files while players stay connected, and runs the join callback
for those players again — the new title should appear immediately.

Two rules about reloading, from [Runtime](/concepts/runtime/):

- **Reload keeps existing chunks.** Edits to `world.on_generate` affect newly
  generated terrain only. For a fresh map, delete the world folder (a lite
  server keeps it in `<pack>/data/world`).
- **Restart after editing `citadel.yml`.** The manifest is read once at boot.

As a next exercise, add a `/hello` command that sends a message to the player
who uses it, then a second argument with a type — the pattern is in
[Commands](/systems/commands/).

## Where to go next

Each of these takes one idea from this page and goes deep:

- [Terrain generation](/world/terrain-generation/) — chunks, deterministic
  generation, heightmaps, `on_populate`.
- [Commands](/systems/commands/) — typed arguments, tab-completion, permissions.
- [The event model](/concepts/events/) — every `on_*` subscription, cancellation,
  and the ask handlers.
- [Guides](/guides/guide-build-a-cottage/) — full builds and games, step by step.

## See also

- [Pack anatomy](/concepts/pack-anatomy/) — every manifest key, assets, dimensions.
- [Runtime](/concepts/runtime/) — reload semantics, tasks, budgets.
- [Cookbook](/cookbook/cookbook-teleport-pads/) — small, complete patterns to copy.
