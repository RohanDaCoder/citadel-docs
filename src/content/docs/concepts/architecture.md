---
title: 'Architecture'
description: 'How a Citadel server is put together — the main room, per-room tables, ticks and the scheduler, chunks and loading, the pack lifecycle, and what happens on reload.'
---

:::note[In short]
one Citadel server hosts a **main room** (and any rooms you
create), runs each loaded pack's entry script in its own VM, and drives
everything from a 50 ms world tick plus a script scheduler. This page lays
out the machine model the rest of the docs assume: which table belongs to
which room, when callbacks run, how chunks come and go, and what reload
actually replaces.
:::

## The server, rooms and per-room tables

A server has one **main room** at boot, and a pack can make more with
`rooms.create{}`. Each room owns its own copy of the six room tables:

| Room table | Covers |
| --- | --- |
| `world` | the room's blocks, entities, displays, screens and time |
| `players` | who is in that room, and their room-scoped events |
| `ui` | UI broadcast to everyone in the room |
| `game` | that room's registries and spawn settings |
| `rooms` | making and destroying rooms |
| `sound` | sound heard in the room |

The lowercase globals you use at the top of a script belong to the **main
room**; `rooms.create{}` returns a room handle whose fields (`room.world`,
`room.players`, ...) are that room's own tables. Everything else — `fx`,
`commands`, `time`, `task`, `http`, `storage`, `stores`, `shop`, `hub` — is
server-wide. A player is in exactly one room at a time; `player.room` is
`nil` while they are between rooms.

## Ticks, tasks and the scheduler

The world advances in 50 ms ticks. Two clocks drive pack code:

- **`time.on_tick(fn)`** — runs `fn(tick)` once per world tick for work tied
  to the simulation. Missed ticks coalesce: remaining listeners resume with
  the latest tick number.
- **`task.wait` / `task.delay` / `task.spawn`** — the script scheduler.
  `task.wait` uses elapsed **real time**, resumed once the requested time has
  passed and the scheduler can run, without rounding to Minecraft's ticks.

`spawn`, `delay` and `defer` accept a function or a suspended coroutine,
forward all arguments, and return the coroutine. `time.every` is a repeating
timer that returns a connection and may cancel itself inside its callback.
The full task semantics — including the initialization exception — are in
[Runtime](/concepts/runtime/).

## The pack lifecycle

A pack is a folder: a `citadel.yml` manifest, an entry script, and whatever
else it `require`s or ships (assets, world folders, layouts). At boot:

1. The server reads its own `citadel.yml` (mode, game version, bind ports).
2. Packs load; each manifest's keys are checked — an unknown key stops the
   server with the field named.
3. Each pack's entry script runs in its own VM. The entry has **5 seconds**
   of work between two waits and **30 seconds** in all; past that the load
   fails and the log says why. Big scenery is built once at load and pasted
   per chunk, never block-by-block at load.
4. Initialization commits: recipes, assets, layouts, block/entity
   registrations, commands, model registrations, asks and spawn settings all
   register at once. Tasks spawned during load start only after this commit.
5. The port opens; players join. The chunks around the spawn are generated
   before the port opens.

A failed entry script discards its drafts and the previous script keeps
running (see [Reload](#reload) below).

## Chunks: loading, unloading, determinism

**Chunks nobody is near are unloaded.** Every ten seconds the server drops
chunks beyond the view distance of all players and entities. When someone
returns, a stored world loads the chunk from disk; a `script` world calls
`on_generate` again.

:::caution[Gotcha]
`world.on_generate` must therefore make the **same blocks every
time** for the same chunk. Draw from a hash of the position, never
`math.random`. A script-world chunk changed live (`world.set_block`,
`world.fill`) stays in memory and is not regenerated.
:::

Where the world lives on disk: a full server keeps it in `world/` beside the
server's `citadel.yml` (the world is the server's — removing a pack does not
take the map). A lite server keeps it in the first pack, `<pack>/data/world`.
A dimension is a folder beside the main world (`world_dungeon`). The
`world` manifest key decides where chunks come from — `script`, `overworld`,
a world folder, or "ask the scripts first" when the key is absent. All of it
is in [Pack anatomy](/concepts/pack-anatomy/#the-world-key) and
[Rooms and dimensions](/concepts/rooms-and-dimensions/).

## Events and asks

Pack code reacts through `on_*` subscriptions that return a connection
(`connection:cancel()` unsubscribes), with one deliberate exception:
`world.on_generate` and `world.on_populate` are single-handler **setters** —
a later call replaces the previous handler and returns nothing.

Most events are notifications. Three are **asks** — cancellable questions the
engine asks a few milliseconds before acting: `players.on_break`,
`players.on_place` and `players.on_damage`. No answer in time denies the
action; a listener that returns `nil` still allows it. Miss too many and the
engine stops asking that kind. The whole model is in
[The event model](/concepts/events/).

## Reload

Saving any `.luau` file in the pack, at any depth, restarts the pack's script
while the server keeps running:

- Players stay connected, and the join callbacks run for them again.
- Initialization re-registers everything atomically; a failed entry discards
  the drafts and resumes the old script.
- Local storage is flushed before the replacement loads; the old VM finishes
  cleanup first.
- Existing chunks are **not** regenerated — `on_generate` edits apply to new
  terrain only. Restart (or delete the world folder) for a fresh map.
- `citadel.yml` is read at boot only: manifest changes need a restart.

The tick budget and every other limit around reload are collected in
[Limits](/systems/limits/).

## Identity and connections

A player's identity comes from one of three places: a proxy signing it
(`MODERN_FORWARDING_SECRET`), Mojang verification (`online_mode: true`, the
default), or nobody (`online_mode: false`, where anyone can join with any
name). Bedrock clients connect over RakNet/UDP or NetherNet, driven by the
server file's `bind` keys. Every Java client 1.8–26.x joins the same server;
feature differences are per-player facts (`player:supports`), never script
branches on a version number.

## See also

- [Pack anatomy](/concepts/pack-anatomy/) — the manifest, files and assets.
- [Runtime](/concepts/runtime/) — tasks, modules and budgets in depth.
- [The event model](/concepts/events/) — subscriptions, cancellation, asks.
- [Rooms and dimensions](/concepts/rooms-and-dimensions/) — more rooms, more worlds.
- [Server settings](/systems/server-settings/) — the server's own `citadel.yml`.
