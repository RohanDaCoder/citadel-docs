# SOURCE: Storage

`storage.status()` returns `{ pending: boolean, error: string? }`. A write
failure remains visible and is retried. `storage.flush()` yields until the
current values are saved, or raises the write error. Call it from a callback
or `task.spawn`, after initialization. `storage.set` changes memory immediately;
unflushed changes can still be lost if the process crashes.
Strings and record keys in JSON-backed storage must be valid UTF-8; invalid
bytes raise an error instead of being replaced. Use `stores.open():blob_put` for
binary data. The UTF-8 rule also applies to persistent entity and block data
and other JSON-backed APIs.
A value it cannot hold is an error that names it, never a changed copy:

```luau
local t = { 1, 2 }; t.total = 3
storage.set("score", t)
-- error names score and total: mixed lists and records have no JSON shape.

storage.set("tick", function() end)
-- error: storage cannot save tick: a function is not a JSON value...
```

- Records use string keys; lists must be contiguous from index 1. A table cannot mix the two.
- Numbers must be finite, and cyclic tables raise an error before changing stored data.
- Persistent data views are accepted directly; reads return detached plain tables.
- Only `nil` deletes. `{}` saves and reads back as an empty table.
