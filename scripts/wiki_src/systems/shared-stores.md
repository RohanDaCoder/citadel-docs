---
title: Shared stores
section: systems
order: 3
description: The experience-wide durable store — stores.open and the DurableStore calls, versions and conflict errors, fencing-token leases, player blobs, every size limit, and the rules of calling a store that yields.
tags: [stores, durability, versions, conflicts, leases, blobs, limits]
---

# Shared stores

> **In short:** `stores.open` returns the one store an experience shares —
> every instance, and the development workload, see the same facts and blobs.
> Writes are versioned (a conflict is a structured error your `pcall` sees),
> leases hand out fencing tokens, and blobs keep per-player binary data. Every
> call yields while the I/O runs, so there are calling rules and a
> 32-pending-requests cap.

## One store per experience

On Minefort, a development workload and all instances of its experience share
one store. **A pack cannot choose another store.** When `CITADEL_STORE` names
a socket, that socket must work or the call fails. The first call logs which
store opened, and where.

```luau
local scores = stores.open()
players.on_join(function(player)
    local visits = scores:increment("visits", 1)
    player:message("Visit number " .. tostring(visits))
end)
```

`stores.open()` returns the experience's store. **Passing an id is an
error.** The `storage` API, by contrast, stays a local per-pack JSON file even
in a published world — see [Storage](/wiki/storage).

## The calls

| Call                                                           | Returns                 | Purpose                                                |
| -------------------------------------------------------------- | ----------------------- | ------------------------------------------------------ |
| `stores.open()`                                                | `DurableStore`          | The experience's one store; no id.                     |
| `handle:get(key)`                                              | `(value, version)`      | A fact's value; version zero means absent.             |
| `handle:set(key, value, if_version, lease?)`                   | new version             | Writes a fact if its version is still `if_version`.    |
| `handle:delete(key, if_version, lease?)`                       | —                       | Removes a fact if its version is still `if_version`.   |
| `handle:increment(key, by)`                                    | number                  | Atomically increments a number, starting at zero.      |
| `handle:list(prefix?, cursor?, limit?)`                        | `(keys, next_cursor)`   | Fact keys with this prefix, a page at a time.          |
| `handle:blob_get(player_uuid, key)`                            | `(string?, version)`    | One player's binary blob, or nil.                      |
| `handle:blob_put(player_uuid, key, bytes, if_version, lease?)` | new version             | Writes one player's binary blob.                       |
| `handle:blob_delete(player_uuid, key, if_version, lease?)`     | —                       | Deletes one player's blob.                             |
| `stores.blob_list(player_uuid)`                                | entries                 | A player's blobs across all blob stores in this scope. |
| `stores.lease(key, holder, ttl_ms)`                            | number                  | Takes a lease; returns a fencing token.                |
| `stores.renew(key, token)`                                     | —                       | Extends the lease that `token` holds.                  |
| `stores.release(key, token)`                                   | —                       | Gives up the lease that `token` holds.                 |
| `stores.request(query, bytes?)`                                | `(answer, blob_bytes?)` | Sends one raw query; yields until it answers.          |

`stores.blob_list` returns entries across all blob stores in this scope, each
with its store, key, version and size. `handle:list` returns the cursor for
the next page, or nil at the end.

**Facts and blobs have separate keys:** a fact `"world"` and a blob `"world"`
are different values.

## Versions and conflicts

`get` returns the value with its version — **version zero means absent**.
`set` and `delete` take `if_version`: the write only lands if the version is
still the one you read. A mismatch is a conflict, not a silent overwrite.

`pcall` preserves the value passed to `error`, including tables, numbers and
booleans; native binding errors remain readable strings. Store errors reach
`pcall` as a table:

| Error table                                     | Meaning                                                         |
| ----------------------------------------------- | --------------------------------------------------------------- |
| `{err = "conflict", version = current_version}` | The version you read is stale — read again and retry.           |
| `{err = "held", by = current_holder}`           | The fencing token is stale — the lease is held by someone else. |

> **Gotcha:** after an I/O timeout, a write may have committed. Retry only
> versioned writes, never an increment.

## Leases

`stores.lease(key, holder, ttl_ms)` returns a **fencing token**; `renew` and
`release` maintain the lease. Leases last up to **one hour**, and there are at
most 100,000 issued lease tokens. A stale fencing token fails with
`{err = "held", by = current_holder}` — the `lease?` argument of `set`,
`delete`, `blob_put` and `blob_delete` ties the write to a token you hold.

## Blobs

Blobs are per-player binary values, keyed by the player's uuid — use them
where JSON cannot hold the data (see the UTF-8 rule in
[Storage](/wiki/storage)). At most 32 MiB a blob, and each player may have at
most 1,000 blobs.

> **Note:** hosted blobs are not in world archive backups.

## Limits

| Limit                         | Value                                                                |
| ----------------------------- | -------------------------------------------------------------------- |
| Keys                          | at most 256 bytes                                                    |
| Facts                         | at most 1 MiB                                                        |
| Blobs                         | at most 32 MiB                                                       |
| Hosted storage per experience | 512 MiB, and 1 MiB more for every Java player who has ever joined it |
| Number of values              | no limit                                                             |
| Blobs per player              | at most 1,000                                                        |
| Lease tokens                  | at most 100,000 issued; leases last up to one hour                   |
| Pending requests per pack     | at most 32                                                           |

## Where the data lives without a socket

**Without a socket, data lives in files that survive a restart.** Every local
run works this way.

- Facts are in `data/store/00000000-0000-0000-0000-000000000000.json`.
- A blob is a file under
  `data/store/blobs/<player-uuid>/00000000-0000-0000-0000-000000000001/`.
- **Writes are atomic.** A killed server keeps the previous value.
- `store_dir` in `citadel.yml` moves that directory. Two servers on one laptop
  need two directories (see [Server settings](/wiki/server-settings)).

## Calling rules

Every call yields while the I/O runs; other callbacks continue meanwhile.

- Call from scripts, callbacks or tasks.
- **Do not call from synchronous ask handlers or at module initialization.**
- A pack can have up to **32 pending requests**.

> **Tip:** a `task.spawn` around a store call at startup keeps module load
> from blocking on I/O — the pattern [Runtime](/wiki/runtime) describes for
> the initialization exception.

A world release rollback does not rewind shared facts or blobs — treat store
writes as external effects that survive (see [Runtime](/wiki/runtime#reload-exactly)).

## See also

- [Storage](/wiki/storage) — the local per-pack JSON store, and when it is
  the better fit.
- [Shop](/wiki/shop) — purchase delivery uses the same retry rules.
- [Server settings](/wiki/server-settings) — `store_dir` moves the store
  files.
- [`DurableStore`](/ref/DurableStore) — the reference entry for the handle.
- [Limits](/wiki/limits) — every numeric limit in one place.
