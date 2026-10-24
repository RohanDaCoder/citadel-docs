---
title: 'FAQ and troubleshooting'
description: 'The questions that come up when a pack misbehaves — load failures, silent reloads, mobs that do not spawn, commands that vanish, stores that error, and what the log is telling you.'
---

:::note[In short]
almost every Citadel surprise is one of these: a budget was
exceeded, a reload changed more than expected, a version lacked a feature,
or an options field was misspelt. Work down this page with the server log
open — Citadel's errors name the field, the file and the nearest valid
spelling.
:::

## The pack will not load

**The log says the load failed.** The entry script has **5 seconds** of work
between two waits and **30 seconds** in all. Build big scenery once at load
and paste it per chunk — do not loop over every block of every level at load.
If the entry script fails, its drafts are discarded and the previous script
resumes (see [Runtime](/concepts/runtime/)).

**The server stops on an unknown key.** Manifest keys — in both the pack's
and the server's `citadel.yml` — are checked at boot; an unknown key or mode
stops the server with the field named. `rooms.create` options are checked the
same way at runtime.

**Packs name different modes.** Packs that name different modes in their
manifests, or that all name none, stop the server. The message says how to
set one: a `--lite`/`--full` flag, or `mode` in the server file.

## I edited the script and nothing changed

Saving any `.luau` file restarts the pack's script — but:

- **Existing chunks are kept.** Edits to `world.on_generate`, `seed` or
  `terrain` apply only to chunks generated from here on. For a fresh map,
  stop the server and delete the world folder; the log names it the first
  time a script world reloads.
- **`citadel.yml` is read at boot only.** Manifest changes need a restart.
- **`players.on_join` runs again for every online player.** Make it safe to
  run twice (see [Runtime](/concepts/runtime/)).
- **A spawn/drops/attacks value the new script does not set is removed** —
  set it again in the new run (see [Game data](/world/game-data/)).

## My calls error with "no option"

Options tables are strict: **an unknown field is an error** that names the
nearest valid one — `colour` suggests `color`; a field of the wrong type is
also an error. Check the signature in the [API reference](/ref/) and remember
the API spells it `color` (and `colors.gray`), `at` for positions, `from`/`to`
for box corners. See [Conventions](/concepts/conventions/).

## Mobs do not spawn

On a `mode: lite` world — and in every room made by `rooms.create` — **no mob
spawns by itself**. Switch a kind on with `game.entities.<kind>.spawn = true`
(make sure the world has biomes; a script world spawns nothing on 1.8.9), or
spawn directly with `world.spawn(name, pos)`:

- `spawn = false` stops natural spawning only — spawners, `/summon`,
  `world.spawn` and breeding still work.
- A zombie from `world.spawn` does not hurt players until `spawn = true`,
  `attacks = true`, or the room has the `damage` rule.
- a0.1.0 to a0.1.3 have no natural spawning at all: every write is an error.
- The full tri-state rules are in [Game data](/world/game-data/) and
  [Mobs](/entities/mobs/).

## Blocks do not drop / players take no damage

- Block drops by the world (a torch whose wall is gone, decay, explosions)
  are **off by default on lite worlds**; write the block's `drops = true`
  field, or switch survival on with `world.rules{ survival = true }`. A
  player's dig is a different thing — see the next item.
- A dig reaches no block without `survival`, or in the `gamemode: 2`
  (adventure) the quick start uses.
- Anything that is not a rule is the pack's job: `player:damage` for a hit,
  `player.health` to heal, `players.on_death` and `players.on_respawn` for
  what happens next (see [Health](/players/health/)).
- A refused action you did not veto yourself is usually an **ask deadline**:
  a handler that errors or runs over two milliseconds counts as a missed
  deadline, and protection fails closed. Never `task.wait` in an ask; miss a
  kind too often and the engine stops asking (see
  [The event model](/concepts/events/)).

## The command exists but nobody sees it

- **`permission`:** without the node, a player neither sees nor runs the
  command — and `/help` lists only what the player may run.
- **One pack owns a name** in a room: a second pack that adds the name or an
  alias is the conflict the log names.
- A required argument never follows an optional one; check the usage grammar
  in [Commands](/systems/commands/).

## Store calls error or hang

- Every `stores` call **yields** — call from a callback or `task.spawn`,
  never from a synchronous ask handler or at module initialization.
- At most **32 pending requests** per pack: batch writes in a task.
- A version conflict reaches `pcall` as `{ err = "conflict", version = ... }`;
  a stale fencing token as `{ err = "held", by = ... }`. Re-read and retry —
  see [Shared stores](/systems/shared-stores/).
- `storage.flush()` may only run from a callback or `task.spawn`, after
  initialization.

## `nil` where a number should be

What a game version lacks is **absent, not zero**: `player.food` is `nil` on
Alpha, `game.block(name)` returns `nil` for a block the game lacks, an
unknown particle name sends nothing. Check for `nil` before arithmetic —
[Conventions](/concepts/conventions/#what-a-version-lacks-is-absent).

## Performance: the budget

`citadel.budget()` tells you where the time went (`used`, `peak`, `skipped`,
`dropped`, `slowest`), `citadel.on_slow` names the hook at most once a
second, and the server log reports a slow pack at most once every five
seconds. Going over is not an error — do less per tick or raise `budget_ms`.
The full diagnosis guide is [Limits](/systems/limits/).

## Where the log is

`citadel.log(...)` writes under the pack's name. Callback errors are logged
with file and line automatically. The first store call logs which store
opened and where; the first script-world reload logs the world folder's path.

## See also

- [Runtime](/concepts/runtime/) — load and reload semantics in full.
- [Limits](/systems/limits/) — every budget and queue.
- [The event model](/concepts/events/) — ask deadlines and disabled kinds.
- [API reference](/ref/) — signatures for every call.
