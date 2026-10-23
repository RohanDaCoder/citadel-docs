---
title: What is Citadel
section: getting-started
order: 1
description: Citadel is Minefort's Luau scripting engine for Minecraft servers — one pack runs unchanged on every Java client from 1.8 to 26.x, as the whole game (lite mode) or as a plugin over survival (full mode).
tags: [overview, platform, modes, hosting]
---
# What is Citadel?

> **In short:** Citadel is a scripting engine for Minecraft servers, built by
> Minefort. You write **packs** — folders of Luau (Lua) files plus a
> `citadel.yml` manifest — and the engine runs them as a game server that every
> Java client from 1.8 to 26.x can join. A pack either **is** the whole game
> (`mode: lite`) or **adds to** vanilla survival (`mode: full`).

## The one-paragraph model

Citadel replaces the plugin/mod ecosystem with a single scripting API. There is
no Java to compile, no per-version builds, no Spigot/Paper fork to track. Your
pack calls globals — `world`, `players`, `ui`, `game`, `commands`, `fx`,
`sound`, `http`, `stores` and about twenty more — and Citadel translates those
calls into the right packets for each client version. The same pack serves a
1.8.9 client and a 26.x client from one server. Where a client cannot show a
feature, the API degrades on its own: a call that cannot render is simply not
sent, and you can query support per player with `player:supports`.

## Three ways a pack can run

The `mode` key in a pack's manifest says **who owns the game**:

| Mode | Meaning |
| --- | --- |
| `mode: lite` | Your scripts are the game. No survival: no natural mob spawning, no block drops, no health rules — unless you switch each on with `world.rules` or per-kind fields. Terrain comes from your `world.on_generate` (or a world folder). |
| `mode: full` | **Citadel plays survival** — terrain, health, hunger, mining, inventory, mobs, world rules — and your pack *adds* to it: a shop, a scoreboard, a custom drop. |
| no `mode` key | The pack runs on either kind of server, like a plugin. Useful for packs that work everywhere. |

The server decides its mode in this order: a `--lite`/`--full` flag, then the
server's own `citadel.yml`, then what the packs' manifests agree on, and
finally survival when there are no packs. A `--lite` server with no packs runs
an empty world and no game.

## Where Citadel runs

- **Locally**: a `citadel` binary on your machine. `citadel --lite --pack ./first`
  starts a server on `localhost:25565` you join from Minecraft Java Edition.
- **On Minefort**: a *development workload* builds an **experience**; its
  instances are the published copies players join. `citadel.env` tells a script
  which copy it is on (`"development"`, `"unlisted"`, `"published"`).
- On Minefort, a development workload and all instances of its experience share
  one data store (see [Shared stores](/wiki/shared-stores)).

## Game versions

The engine emulates the game version you pick, not just the newest one:

- `game: "1.8.9"` (the default) and `game: "a0.1.0"` (Alpha) are the named
  versions a server file may choose. Blocks, items and entity kinds come from
  that version's own registry — `game.block(name)` returns `nil` for a block
  the game lacks.
- Every Java client from **1.8 to 26.x** can join the same server. The script
  never sees a client version; it asks `player:supports("display")` and the
  like (see [Client versions](/appendix/client-versions)).
- What a version lacks is **absent, not zero**: on Alpha, `player.food` is
  `nil` because there is no food rule there.

## What is in the API

The API surface, all documented in this wiki's [API reference](/ref):

- **World** — terrain generation (`world.on_generate`), block reads/writes,
  builds and schematics, zones, raycasts, pathfinding, lighting.
- **Players** — lifecycle events, movement, inventory, visibility, health,
  per-player UI.
- **Entities** — custom entities with think loops and physics, mob spawning
  rules, NPCs.
- **UI** — titles, chat, boss bars, screens, canvases, menus, dialogs,
  layouts, displays, particles, sound.
- **Systems** — commands with tab-completion, permissions, per-pack storage,
  experience-wide stores with leases, HTTP, WebSockets, Gem shop, hub
  discovery, rooms and dimensions.

## See also

- [Quick start](/wiki/quick-start) — a working pack in five minutes.
- [Architecture](/wiki/architecture) — how the engine runs your script.
- [Pack anatomy](/wiki/pack-anatomy) — every `citadel.yml` key.
- [Tooling](/wiki/tooling) — strict types with `citadel.d.luau` and `luau-lsp`.
- [Conventions](/wiki/conventions) — the rules every API call follows.
- [Client versions](/appendix/client-versions) — the per-feature version matrix.
