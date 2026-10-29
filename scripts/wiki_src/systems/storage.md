---
title: Storage
section: systems
order: 2
description: The per-pack local JSON store — storage.get/set/keys by key in the pack's storage.json, what a JSON value may be, the UTF-8 rule, atomic writes, and storage.status/flush for when a write fails.
tags: [storage, json, persistence, flush, utf-8]
---

# Storage

> **In short:** `storage` is a pack's own local key–value store, saved as JSON
> in its `storage.json` — values a pack keeps between restarts. This page
> covers the five calls, what a value may be (the JSON shape rules), the
> UTF-8 rule for strings and keys, and `storage.status`/`storage.flush` for
> tracking and forcing the save. For data shared across every server of an
> experience, see [Shared stores](/wiki/shared-stores).

## The calls

| Call                                   | Returns              | Purpose                                                          |
| -------------------------------------- | -------------------- | ---------------------------------------------------------------- |
| `storage.get(key: string)`             | any                  | The value saved under `key`, or nil when there is none.          |
| `storage.set(key: string, value: any)` | —                    | Saves a value under `key`; nil forgets it.                       |
| `storage.keys(prefix: string?)`        | `{ string }`         | Every key, sorted; with a prefix, only those that start with it. |
| `storage.status()`                     | `{ pending, error }` | Last persistence error and whether there are unsaved changes.    |
| `storage.flush()`                      | —                    | Yields until saved; raises an error on failure.                  |

`storage.set` changes memory immediately; unflushed changes can still be lost
if the process crashes. **Only `nil` deletes** — `{}` saves and reads back as
an empty table.

## What a value may be

Storage is JSON-backed, so a value must have a JSON shape. A value it cannot
hold is an error that names it, never a changed copy:

```luau
local t = { 1, 2 }; t.total = 3
storage.set("score", t)
-- error names score and total: mixed lists and records have no JSON shape.

storage.set("tick", function() end)
-- error: storage cannot save tick: a function is not a JSON value...
```

The shape rules:

- Records use string keys; lists must be contiguous from index 1. A table
  cannot mix the two.
- Numbers must be finite, and cyclic tables raise an error **before changing
  stored data**.
- Persistent data views are accepted directly; reads return detached plain
  tables.

## The UTF-8 rule

Strings and record keys in JSON-backed storage must be valid UTF-8; invalid
bytes raise an error instead of being replaced. Use
`stores.open():blob_put` for binary data — see
[Shared stores](/wiki/shared-stores#blobs).

> **Note:** the UTF-8 rule also applies to persistent entity and block data
> and other JSON-backed APIs.

## Saving, status and flush

`storage.status()` returns `{ pending: boolean, error: string? }`. A write
failure remains visible and is retried.

`storage.flush()` yields until the current values are saved, or raises the
write error. Call it from a callback or `task.spawn`, **after initialization**
— not at the top level of the entry script.

> **Gotcha:** a failed flush raises the write error; the values stay pending
> and the failure stays visible in `storage.status().error` until a retry
> succeeds.

On a script reload, local storage is flushed before the replacement loads
(see [Runtime](/wiki/runtime#reload-exactly)).

## When to use storage, and when a shared store

The `storage` API stays a **local per-pack JSON file, even in a published
world**: each server of the experience has its own copy, and nothing is
shared. Use it for per-pack state that one server owns outright — a pack's
own settings, a local cache, a leaderboard the pack computes alone.

Use [Shared stores](/wiki/shared-stores) when several servers — every
instance of an experience, or a development workload and its instances — must
read and write the same facts, or for blobs and leases.

## See also

- [Shared stores](/wiki/shared-stores) — the experience-wide store, with
  versions, conflicts, leases and blobs.
- [Runtime](/wiki/runtime) — the reload rules that flush storage first.
- [Limits](/wiki/limits) — the tick budget, and where every numeric limit
  lives.
