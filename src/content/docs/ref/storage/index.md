---
title: 'storage global'
description: 'A per-pack JSON file that survives a restart.'
---

A per-pack JSON file that survives a restart.

Part of the [Storage](/systems/storage/) article.

## Functions

| Call | Purpose |
| --- | --- |
| [`status`](/ref/storage/status/) | Last persistence error and whether there are unsaved changes. |
| [`flush`](/ref/storage/flush/) | Yields until saved; raises an error on failure. After initialization only. |
| [`get`](/ref/storage/get/) | Returns the value saved under `key`, or nil when there is none. |
| [`set`](/ref/storage/set/) | Saves a value under `key` in this pack's storage.json; nil forgets it. |
| [`keys`](/ref/storage/keys/) | Every key, sorted; with a prefix, only those that start with it. |
