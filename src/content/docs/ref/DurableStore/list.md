---
title: "durableStore:list"
description: "Returns fact keys with this prefix and the cursor for the next page, or nil at the end."
---

Part of [`DurableStore`](/ref/DurableStore/).

```luau
durableStore:list(prefix: string ?, cursor: string ?, limit: number ?) → ({ string }, string ?)
```

Returns fact keys with this prefix and the cursor for the next page, or nil at the end.

## Parameters

| Name     | Type     | Required |
| -------- | -------- | -------- |
| `prefix` | `string` | no       |
| `cursor` | `string` | no       |
| `limit`  | `number` | no       |

## Returns

- `({ string }, string ?)`
