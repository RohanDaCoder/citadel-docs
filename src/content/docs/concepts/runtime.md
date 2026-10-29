---
title: 'Runtime'
description: 'The script runtime in detail — task.spawn/wait/delay/defer semantics, the initialization exception, require and modules, the tick budget, what reload keeps and discards.'
---

:::note[In short]
each pack runs as one Luau VM with a cooperative scheduler.
This page covers the task library's exact semantics, how `require` resolves
modules, the per-pack tick budget and what happens when it runs out, and the
precise rules of a hot reload.
:::

## Tasks: `spawn`, `delay`, `defer`, `wait`

`task.spawn`, `task.delay` and `task.defer` accept either a function or a
suspended coroutine, forward all arguments (including nils), and return that
coroutine:

| Call                       | Runs                                                            |
| -------------------------- | --------------------------------------------------------------- |
| `task.spawn(fn, ...)`      | Immediately, until the task yields or returns.                  |
| `task.delay(sec, fn, ...)` | After `sec` seconds of elapsed real time.                       |
| `task.defer(fn, ...)`      | On the next scheduler turn.                                     |
| `task.wait(sec)`           | Yields the calling thread until `sec` real seconds have passed. |

- `task.wait` and `task.delay` measure **elapsed real time**, in full and lite
  mode alike. Unlike Roblox's heartbeat scheduling they resume once the time
  has passed and the scheduler can run them — not rounded to Minecraft's 50 ms
  ticks. Use `time.on_tick` for work tied to world ticks.
- Zero or negative seconds yield until the next scheduler turn.
- The actual wait may be longer under load. Durations must be finite and
  within the supported clock range; invalid values raise catchable errors.
- `time.every(sec, fn)` is a repeating timer that returns a connection and may
  cancel itself inside its callback.
- `task.cancel` works on a suspended task, also after `task.wait`; cancelling
  a **running** thread is an error. Cancelling stops the task's code but
  cannot undo I/O it already submitted.

## The initialization exception

Tasks spawned, deferred or delayed **while `main.luau` loads** start only
after initialization commits — the pack's startup is atomic:

- The top level of `main.luau` may `task.wait`, but it cannot wait for one of
  those child tasks to finish before startup completes.
- If the entry script fails, the drafts are discarded and the previous script
  (if any) resumes.

## Modules and `require`

`require` splits a pack into files:

- Resolves from the **pack root** (`require("util/math")` is
  `<pack>/util/math.luau`).
- Caches by canonical file path; a module returning `nil` is cached as `true`.
- Rejects cycles, and rejects symlinks that lead outside the pack.
- `loadstring`, `getfenv` and `setfenv` are not there — a pack cannot run text
  as code or reach another environment.

:::caution[Gotcha]
a module's top level may not call `task.wait`, and synchronous
ask handlers may not either. Ordinary event callbacks, `main.luau` and task
threads may.
:::

## The tick budget

A pack's tick and event callbacks share part of each tick, set with
`budget_ms` in the pack's `citadel.yml`. The default is **2 ms**.

| Covered by the budget                                                               | Not covered (100 ms runaway limit instead)                                      |
| ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| `time.on_tick`, `time.every`, survival events (`world.on_block_break` and the rest) | `players.on_join`, input events (`on_click`, `on_chat`, commands), task threads |
|                                                                                     | Chunk callbacks keep their separate **2 s** limit                               |

It counts work, not time spent waiting. When the budget runs out mid-batch:

- Ordinary events retain their arguments and remaining listeners until the
  next budget window; cancelling a subscription also removes its pending
  delivery.
- `time.on_tick` coalesces missed ticks — listeners resume with the latest
  tick number, no replay.
- Socket messages stay queued until their callback can run; a `time.every`
  timer that does not fit keeps its place among due timers.
- **Nothing is killed.** A started callback always finishes. Going over is not
  an error — do less per tick, or raise `budget_ms`.

Each pack retains at most **4096 ordinary events**; overflow drops the oldest
and logs the pack. Joins, leaves, deaths and respawns are retained in order
and never evicted — they carry the original player session, so a delayed
leave still has its `player.data` after a reconnect. This is in-process
delivery, not a durable journal across a crash: keep lifecycle callbacks
short.

## Reading the numbers

```luau
local b = citadel.budget()
print(b.of)        -- 2, the ms this pack gets per tick
print(b.used)      -- what the last tick spent
print(b.peak)      -- the most any tick has spent
print(b.skipped)   -- callbacks not run for want of budget, since the script started
print(b.dropped)   -- events this pack never saw (overflowed the 4096 queue)
print(b.slowest)   -- { hook = "on_tick", ms = 4.1 }, or nil
print(b.asks)      -- what the engine's questions cost this pack; see "asks"

citadel.on_slow(function(slow)
    print(slow.hook, slow.used, slow.of, slow.skipped)   -- "on_tick" 2.4 2 3
end)
```

`citadel.on_slow` runs at most once a second; hook names are `"on_tick"`,
`"every"`, or the event's name (`"block_break"`, `"pickup"`). The server log
shows the pack, hook and time at most once every five seconds.

## Reload, exactly

Saving any `.luau` file in the pack, at any depth, restarts the pack's script.
The server keeps running:

- Players stay connected; `players.on_join` runs again for every online
  player — **make it safe to run twice**.
- Initialization stages recipes, assets, layouts, block/entity registrations,
  commands, model registrations, asks, spawn settings and queued world
  actions. A failed entry discards these drafts and resumes the old script.
- The entry must finish within 30 seconds, including any `task.wait` or read
  requests. `task.spawn` work starts after successful initialization.
- Local storage is flushed before the replacement loads; the old VM finishes
  cleanup before the replacement starts callbacks.
- Writes to shared stores, purchase prompts/acks and `storage.flush` belong
  in `task.spawn` or callbacks — external writes cannot be rolled back, so
  existing-world/player side effects belong in callbacks too.
- On success, the old script's timers and connections end.
- **The world stays.** Every existing chunk stays, in script and terrain
  worlds. A changed `world.on_generate`, `seed` or `terrain` applies only to
  chunks generated from here on. To regenerate the whole map: stop the
  server, delete the world folder (the log names it), start again.
- A script reload removes a spawn/drops/attacks value that the new script
  does not set again (see [Game data](/world/game-data/)).
- A mob a pack spawned stays when the script reloads; an NPC does not.

## See also

- [Architecture](/concepts/architecture/) — the machine around this runtime.
- [The event model](/concepts/events/) — subscriptions, asks, queue semantics.
- [Limits](/systems/limits/) — every numeric limit in one table.
- [Modules and tasks recipes](/cookbook/cookbook-save-load/) — using tasks for
  I/O patterns.
