---
title: Limits
section: systems
order: 9
description: The tick budget — budget_ms and its 2 ms default, what it covers and what keeps the 100 ms runaway limit instead, what happens when it runs out, citadel.budget() fields, citadel.on_slow, the 4096-event queue, and the asks the engine asks.
tags: [budget, limits, on_slow, event queue, asks, performance]
---

# Limits

> **In short:** a pack's tick and event callbacks share a slice of every
> tick — `budget_ms` in the pack's `citadel.yml`, **2 ms by default**. When
> it runs out nothing is killed: events are retained, ticks coalesce, socket
> messages queue. This page covers the budget, `citadel.budget()` and
> `citadel.on_slow`, the 4096-event queue, the asks, and a pointer table to
> every other limit. Reload semantics live in [Runtime](/wiki/runtime#reload-exactly).

## The tick budget

A pack's tick and event callbacks share part of each tick. Set it with
`budget_ms` in the pack's `citadel.yml`. The default is **2 ms**.

| Covered by the budget                                                                   | Not covered                                                                                                               |
| --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `time.on_tick`, `time.every`, the survival events (`world.on_block_break` and the rest) | `players.on_join`, input events (`on_click`, `on_chat`, commands), task threads — these keep the **100 ms runaway limit** |
|                                                                                         | Chunk callbacks keep their separate **2 s** limit                                                                         |

**It counts work, not time spent waiting** — a callback that yields on I/O
does not spend budget while it waits.

## When the budget runs out

When the budget runs out mid-batch:

- **Ordinary events retain** their original arguments and remaining listeners
  until the next budget window. Canceling a subscription also removes its
  pending delivery. The bounded event queue still applies.
- **`time.on_tick` coalesces** missed ticks: remaining listeners resume with
  the latest tick number. It does not replay every elapsed tick.
- **Socket messages stay queued** until their callback can run.
- **A `time.every` timer that does not fit retains its place** among due
  timers.
- **Nothing is killed.** A started callback always finishes.

Going over is not an error. Do less per tick, or raise `budget_ms`.

## Reading the numbers

```luau
local b = citadel.budget()
print(b.of)        -- 2, the ms this pack gets per tick
print(b.used)      -- what the last tick spent
print(b.peak)      -- the most any tick has spent
print(b.skipped)   -- callbacks not run for want of budget, since the script started
print(b.dropped)   -- events this pack never saw; see below
print(b.slowest)   -- { hook = "on_tick", ms = 4.1 }, or nil
print(b.asks)      -- what the engine's questions cost this pack; see below

citadel.on_slow(function(slow)
    print(slow.hook, slow.used, slow.of, slow.skipped)   -- "on_tick" 2.4 2 3
end)
```

| Field       | Meaning                                                                    |
| ----------- | -------------------------------------------------------------------------- |
| `b.of`      | The ms this pack gets per tick — `budget_ms` in citadel.yml; 2 by default. |
| `b.used`    | What the last tick spent.                                                  |
| `b.peak`    | The most any tick has spent.                                               |
| `b.skipped` | Callbacks not run for want of budget, since the script started.            |
| `b.dropped` | Events this pack never saw — overflow of the event queue.                  |
| `b.slowest` | `{ hook = "on_tick", ms = 4.1 }`, or nil.                                  |
| `b.asks`    | What the engine's questions cost this pack; see below.                     |

Hook names are short: `"on_tick"`, `"every"`, or the event's name
(`"block_break"`, `"pickup"`).

> **Note:** `on_slow` runs **at most once a second**. The server log shows
> the pack, hook and time, **at most once every five seconds**.

## The event queue

**`b.dropped` counts lost ordinary events.** Each pack retains at most
**4096 ordinary events**; overflow drops the oldest ordinary event and logs
the pack.

Joins, leaves, deaths and respawns are retained in order and **never evicted
by ordinary traffic or skipped because the tick budget was spent**. They carry
the original player session, so a delayed leave still has its `player.data`
after a reconnect. This is in-process delivery, not a durable journal across a
server crash — keep lifecycle callbacks short so their retained backlog drains
(see [Player lifecycle](/wiki/player-lifecycle)).

## The asks

**`b.asks` counts the engine's questions.** An **ask** is a cancellable
event, such as "may this player break this block". The engine waits a few
milliseconds for the answer. Three exist:

| Ask                 | Kind       |
| ------------------- | ---------- |
| `players.on_break`  | `"break"`  |
| `players.on_place`  | `"place"`  |
| `players.on_damage` | `"damage"` |

With no answer in time, the engine **denies the protected action**. With no
protection listener registered, the action follows the normal game rules. A
listener that completes and returns nil still allows the action; an error or
missing answer does not.

Counters are totals; watch them per kind:

```luau
time.every(60, function()
    for kind, count in citadel.budget().asks.kinds do
        if count.missed > count.answered then
            citadel.log(`slow at {kind}: {count.missed} of {count.asks} missed`)
        end
    end
end)
```

The log names a kind you keep missing. **Miss it too often and the engine
stops asking you that kind.** It then takes the default, logs this once, and
sets `disabled`.

Ask handler rules:

- Answer at once. Never call `task.wait` in one.
- Answering costs tick budget, under the hook name `"ask"`.
- A spent budget does not stop an ask from being answered.

The full ask model — vetoes, deadline behaviour, observe-after-veto — is in
[The event model](/wiki/events#asks-the-cancellable-events).

## Other limits, and where they live

| Limit                                                                                                                                                                  | Where it is documented                                                                       |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Load: 5 s of work between waits, 30 s in all for the entry script                                                                                                      | [Pack anatomy](/wiki/pack-anatomy)                                                           |
| Reload entry: 30 s including `task.wait` and read requests                                                                                                             | [Runtime](/wiki/runtime#reload-exactly)                                                      |
| Chunk callbacks: 2 s; the engine waits 60 s for a chunk                                                                                                                | [Terrain generation](/wiki/terrain-generation), [HTTP](/wiki/http#a-world-from-fetched-data) |
| Store limits: keys 256 B, facts 1 MiB, blobs 32 MiB, hosted 512 MiB + 1 MiB a player, 1,000 blobs a player, 100,000 lease tokens, 32 pending requests                  | [Shared stores](/wiki/shared-stores#limits)                                                  |
| HTTP: 16 MiB an answer, 64 pending and 8 on the wire a pack, 600 requests a minute a server, 8 sockets, 1 MiB a message, 256 messages or 4 MiB a queue                 | [HTTP](/wiki/http#limits)                                                                    |
| Network: label 1–32, member 1–40, slots 1–200, players 1–64, `open` 0–200, `data` 4096 B, `meta` 512 B, `status` 32 chars, 20 instances a region, one `start` a second | [Network](/wiki/network#limits)                                                              |
| Command arguments: ranges and the 100 ms runaway limit                                                                                                                 | [Commands](/wiki/commands), this page                                                        |

The one-table view of every number in the corpus is
[the limits table](/appendix/limits-table).

## See also

- [Runtime](/wiki/runtime) — the scheduler around the budget, and the reload
  rules.
- [The event model](/wiki/events) — asks, vetoes and queue semantics.
- [The limits table](/appendix/limits-table) — every numeric limit in one
  table.
- [`Budget`](/ref/Budget) — the reference entry for the numbers.
