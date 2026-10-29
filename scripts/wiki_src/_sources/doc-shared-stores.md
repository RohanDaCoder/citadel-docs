# SOURCE: Shared stores

On Minefort, a development workload and all instances of its experience share one store. A pack cannot choose another store. When `CITADEL_STORE` names a socket, that socket must work or the call fails.
**Without a socket, data lives in files that survive a restart.** Every local run works this way.
- Facts are in `data/store/00000000-0000-0000-0000-000000000000.json`.
- A blob is a file under `data/store/blobs/<player-uuid>/00000000-0000-0000-0000-000000000001/`.
- Writes are atomic. A killed server keeps the previous value.
- `store_dir` in `citadel.yml` moves that directory. Two servers on one laptop need two directories.
- The first call logs which store opened, and where.
```luau
local scores = stores.open()
players.on_join(function(player)
    local visits = scores:increment("visits", 1)
    player:message("Visit number " .. tostring(visits))
end)
```
Every call yields while the I/O runs. Other callbacks continue.
- Call from scripts, callbacks or tasks. Do not call from synchronous ask handlers or at module initialization.
- A pack can have up to 32 pending requests.
- The `storage` API stays a local per-pack JSON file, even in a published world.
The calls:
- `stores.open()` returns the experience’s store. Passing an id is an error.
- `handle:get(key)` returns `(value, version)`. Version zero means absent.
- `handle:set(key, value, if_version, lease?)` returns the new version.
- `handle:delete(key, if_version, lease?)` removes a value.
- `handle:increment(key, by)` atomically increments a number, starting at zero.
- `handle:list(prefix?, cursor?, limit?)` returns `(keys, next_cursor)`.
- `handle:blob_get(player_uuid, key)` returns `(binary_string_or_nil, version)`.
- `handle:blob_put(player_uuid, key, bytes, if_version, lease?)` returns the new version.
- `handle:blob_delete(player_uuid, key, if_version, lease?)` deletes a blob.
- `stores.blob_list(player_uuid)` returns entries across all blob stores in this scope.
- `stores.lease(key, holder, ttl_ms)` returns a fencing token.
- `stores.renew(key, token)` and `stores.release(key, token)` maintain a lease.
Facts and blobs have separate keys: a fact `"world"` and a blob `"world"` are different values.
Limits:
- Keys: at most 256 bytes. Facts: at most 1 MiB. Blobs: at most 32 MiB.
- Hosted storage per experience: 512 MiB, and 1 MiB more for every Java player who has ever joined it. There is no limit on how many values. Each player may have at most 1,000 blobs.
- 100,000 issued lease tokens. Leases last up to one hour.
- Hosted blobs are not in world archive backups.
`pcall` preserves the value passed to `error`, including tables, numbers and
booleans. Native binding errors remain readable strings. Store errors reach
`pcall` as a table:
- A version conflict is `{err="conflict", version=current_version}`.
- A stale fencing token is `{err="held", by=current_holder}`.
