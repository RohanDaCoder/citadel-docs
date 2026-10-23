---
title: Save and load
section: cookbook
order: 7
description: Choosing and using the three persistence layers — player.data for the session, storage for the pack, stores for the experience — with flush, conflict and reload rules in one place.
tags: [persistence, storage, stores, pattern]
---
# Save and load

> **In short:** Citadel has exactly three persistence layers, and each has a
> clear job: `player.data` for the session, `storage` for per-pack values
> (a local JSON file, atomic writes), and `stores` for the whole experience
> (versioned keys, leases, blobs). This page is the decision table and the
> two working patterns.

## Choosing the layer

| Need | Use | Lifetime | Limits |
| --- | --- | --- | --- |
| Score mid-round, cooldown stamp, team | `player.data` | the player's connection | in-memory |
| Best score, settings, per-pack state | `storage.get/set` | the pack, across restarts | local JSON file, per-pack |
| Cross-server values, purchases, player blobs | `stores:*` | the experience | facts 1 MiB, blobs 32 MiB, 512 MiB hosted |

`player.data` is a plain table — no calls, no yields, gone on reconnect.
`storage` is per-pack even on a published world. `stores` is shared by a
development workload and all instances of its experience, and a pack cannot
choose another store.

## The per-pack layer: `storage`

```luau
-- A best score that survives a restart
players.on_leave(function(player)
    local key = "best." .. player.uuid
    local best = storage.get(key) or 0
    if (player.data.coins or 0) > best then
        storage.set(key, player.data.coins)
    end
end)
```

- `storage.set` changes memory immediately; `storage.get` reads the current
  value. Strings and record keys must be valid UTF-8 — invalid bytes raise an
  error instead of being replaced.
- Writes are atomic; a killed server keeps the previous value. Unflushed
  changes can still be lost if the process crashes.
- `storage.status()` returns `{ pending: boolean, error: string? }` — a write
  failure stays visible and is retried.
- `storage.flush()` yields until the current values are saved, or raises the
  write error. Call it from a callback or `task.spawn`, after initialization.

> **Gotcha:** on a script reload, local storage is flushed **before** the
> replacement loads — so writing from the old script's last breath is safe,
> but writes that belong in the new script must happen in its callbacks.

## The experience layer: `stores`

```luau
local scores = stores.open()

players.on_join(function(player)
    local visits, version = scores:increment("visits." .. player.uuid, 1)
    player:message("Visit number " .. tostring(visits))
end)
```

- Every call **yields** while the I/O runs; other callbacks continue. Call
  from scripts, callbacks or tasks — never from synchronous ask handlers or
  at module initialization.
- `handle:get(key)` returns `(value, version)`; version zero means absent.
- `handle:set(key, value, if_version)` is a compare-and-set — a stale version
  reaches `pcall` as `{ err = "conflict", version = current }`.
- `handle:increment(key, by)` is atomic; a number is the common case.
- A pack can have up to **32 pending requests** — batch your writes in a task
  rather than firing hundreds from one event.

The version check, for read-modify-write that must not race:

```luau
task.spawn(function()
    local coins, version = scores:get("pot")
    local ok, err = pcall(function()
        scores:set("pot", coins + 10, version)   -- fails if another server moved it
    end)
    if not ok and err.err == "conflict" then
        -- re-read and retry
    end
end)
```

## Saving on the clock

Persistence that must not lose more than a minute of play:

```luau
local DIRTY = {}

local function mark(player: Player)
    table.insert(DIRTY, player)
end

time.every(60, function()
    if #DIRTY == 0 then return end
    task.spawn(function()
        for _, p in DIRTY do
            scores:set(`coins.{p.uuid}`, p.data.coins or 0)
        end
    end)
    table.clear(DIRTY)
end)
```

`time.every` never drifts, and moving the writes into `task.spawn` keeps the
timer's callback out of the tick budget's way.

## Binary data: blobs

Player-owned binary (a skin, a screenshot) goes in blob calls, which have
their own keyspace — a fact `"world"` and a blob `"world"` are different
values:

```luau
local bytes = http.get(url):image()          -- binary as a string
scores:blob_put(player.uuid, "banner", bytes)
local saved, version = scores:blob_get(player.uuid, "banner")
```

Each player may have at most 1,000 blobs; hosted blobs are not in world
archive backups.

## See also

- [Storage](/wiki/storage) — the per-pack API in full.
- [Shared stores](/wiki/shared-stores) — every call, lease and limit.
- [Runtime](/wiki/runtime) — the reload flush rule and task rules.
- [Leaderboards](/wiki/cookbook-leaderboards) — scoring on top of these
  layers.
