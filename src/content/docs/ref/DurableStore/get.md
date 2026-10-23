---
title: 'durableStore:get'
description: 'Returns a fact''s value and its version; version 0 means absent.'
---

Part of [`DurableStore`](/ref/DurableStore/).

```luau
durableStore:get(key: string) → (any, number)
```

Returns a fact's value and its version; version 0 means absent.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `key` | `string` | yes |

## Returns

- `( any , number )`
