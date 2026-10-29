---
title: 'durableStore:blob_get'
description: 'Returns one player''s binary blob, or nil, and its version; owner is the player''s uuid.'
---

Part of [`DurableStore`](/ref/DurableStore/).

```luau
durableStore:blob_get(owner: string, key: string) → (string ?, number)
```

Returns one player's binary blob, or nil, and its version; `owner` is the player's uuid.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `owner` | `string` | yes |
| `key` | `string` | yes |

## Returns

- `( string ?, number )`
