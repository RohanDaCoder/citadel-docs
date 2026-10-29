---
title: Pack anatomy
section: concepts
order: 2
description: Everything in a Citadel pack — the citadel.yml manifest key by key, the file layout, sounds and other assets, dimensions, permissions groups, and where the world and its data live on disk.
tags: [manifest, citadel.yml, assets, dimensions, files]
---

# Pack anatomy

> **In short:** a pack is a folder: a `citadel.yml` manifest at its root, one
> entry script, whatever modules it `require`s, and optional folders for
> assets, layouts, world data and dimensions. This page is the complete
> manifest reference and the folder map around it.

## The manifest, key by key

```yaml
# citadel.yml — a pack manifest
name: first # the pack's id; "castle:dungeon" ids are prefixed by it
entry: main.luau # the script that runs
motd: My first Citadel pack # shown in the server list
spawn_point: [0.5, 65.0, 0.5]
gamemode: 2 # 0 survival, 1 creative, 2 adventure
mode: lite # lite | full | absent (runs on either)
world: script # script | overworld | a world folder name
budget_ms: 2 # this pack's slice of each tick (default 2 ms)
```

### `mode` — who owns the game

| Mode          | Meaning                                                                                                                           |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `mode: lite`  | Your scripts are the game. Terrain from `world.on_generate`; no survival rules unless switched on.                                |
| `mode: full`  | Citadel plays survival; the pack adds to it (a shop, a scoreboard, a custom drop). A pack cannot ship survival — it _adds_ to it. |
| no `mode` key | Runs on either kind of server, like a plugin.                                                                                     |

Packs that name different modes, or that all name none, stop the server with a
message saying how to set one. A flag or the server file overrules a pack that
names the other mode — the log names that pack.

### The `world` key

`world` says where a chunk comes from:

| Value                | Chunks come from                                                                                                                                                                                                              |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `"script"`           | `world.on_generate` makes them. A chunk it does not fill is air.                                                                                                                                                              |
| `"overworld"`        | Citadel's terrain: biomes, hills, caves, ores, trees, sea level 63. `seed` pins the map. Scripts only add (`world.on_populate`).                                                                                              |
| a name, e.g. `"hub"` | A world folder in the pack, `<pack>/hub`, made once from a build or a vanilla world. The server reads it chunk by chunk and saves player changes into it. A chunk the folder lacks comes from `world.on_generate`, or is air. |
| no `world` key       | The scripts are asked first. A chunk no script filled is overworld terrain on a full server, air on a lite server.                                                                                                            |

Making a world folder ahead of time (a map too big to make live):

```sh
citadel import builds/lobby.schem <pack>/hub --at -186,48,-236 --spawn 0.5,65,0.5
citadel generate <pack> --from -4096,-6144 --to 4095,6143   # --threads n caps cores
```

`citadel generate` runs one script per core, any map size fits in memory, and
chunks already in the folder are kept — a stopped run continues.

### `dimensions`

A pack adds worlds under `dimensions:`. The name is its id inside the pack
(`castle:dungeon`):

```yaml
dimensions:
  dungeon:
    type: { has_skylight: false, has_ceiling: true, weather: false }
    world: script # or "void" to leave chunks empty
```

Every `type` field is optional and starts from the main world's:
`has_skylight`, `has_ceiling`, `weather`, `ultrawarm`, `bed_works`,
`respawn_anchor_works`, `coordinate_scale`, `fixed_time`, `effects`. A world
with a roof looks like the Nether to a client, one with no sky and no roof
like the End; `effects` picks one of the three yourself. A dimension ticks
after the main world and saves to `world_dungeon` beside it. Full guide:
[A dungeon dimension](/wiki/guide-a-dungeon-dimension).

### `permissions`

The manifest defines permission groups; every player starts in `default`:

```yaml
permissions:
  default: { nodes: [casino.play] }
  vip: { inherits: [default], nodes: [casino.vip] }
  staff:
    {
      inherits: [vip],
      nodes: [minecraft.command.gamemode, "casino.*", "-casino.debug"],
    }
```

Same-name groups in two packs merge; a group that inherits an undefined group,
or one named `operator`, stops the server. The full node syntax is in
[Permissions](/wiki/permissions).

### Other keys

- `spawn_point: [x, y, z]` — where players arrive in the main room. With no
  spawn point, an overworld pack takes the first grass block above sea level,
  ring by ring out from (0, 0); the search runs once and is stored in
  `level.json`.
- `min_client` — refuse clients older than this (e.g. `"1.14"`), instead of
  guarding each feature with `player:supports`.
- `store_dir` — moves where `stores` keeps its files (two servers on one
  machine need two directories). Default `data/store`.
- `terrain` — sets the overworld's step list; only `game: a0.1.0` has one
  (the full step table is in [Terrain generation](/wiki/terrain-generation#the-a010-terrain-steps)).

## The folder map

```
first/
  citadel.yml          the manifest
  main.luau            the entry script
  *.luau               anything the entry requires (pack-root resolution)
  assets/
    sounds/...         "<pack>.<file>" sound names
    (other folders)    go into the resource pack unchanged
                        (assets/<pack>/textures/...)
  hub/                 a world folder, if world: hub
  data/
    world/             a lite server keeps the world here
    store/             stores' files when no platform store was named
  dimension folders    beside the world on the server, not in the pack
```

## Textures of your own

On Java 1.21.4 and later, a pack's own items and blocks can have textures: set
`texture` in `game.items.define` and `game.blocks.define`. The engine adds
them to its resource pack; older clients see the vanilla item or block, and a
client that turned the resource pack down sees them too from then on
(`player:supports("resource_pack")` is `false`). A pack that needs its
textures says so with `min_client`.

## The load budget

The entry script has **5 seconds** of work between two waits (`task.wait`)
and **30 seconds** in all; past that the load fails and the log says why.
Build big scenery once at load and copy it (one tree variant pasted per
chunk); do not loop over every block of every level at load.

## Where the world and its data live

- Full server: `world/` beside the server's `citadel.yml` — the world is the
  server's; removing a pack does not take the map.
- Lite server: `<pack>/data/world`.
- Dimension: a folder beside the main world (`world_dungeon`).
- `level.json` in the world keeps the seed, spawn, time and weather of the
  first run. Changing `seed` later does nothing to an existing world; delete
  the world folder for a new map.

## See also

- [Server settings](/wiki/server-settings) — the _server's_ `citadel.yml`:
  bind ports, game version, operators, online mode.
- [Architecture](/wiki/architecture) — how the manifest is consumed at boot.
- [Runtime](/wiki/runtime) — the load budget in context, reload semantics.
- [Storage](/wiki/storage) and [Shared stores](/wiki/shared-stores) — the
  two persistence APIs and their on-disk layout.
