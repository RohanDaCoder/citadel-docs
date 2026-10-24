---
title: 'storage.status'
description: 'Last persistence error and whether there are unsaved changes.'
---

Part of [`storage`](/ref/storage/).

```luau
storage.status() → { pending: boolean, error: string ? }
```

Last persistence error and whether there are unsaved changes.

## Returns

- `{ pending: boolean , error: string ? }`

## Used in

> "`storage.status()` returns `{ pending: boolean, error: string? }`. A write" — [Storage](/systems/storage/)
