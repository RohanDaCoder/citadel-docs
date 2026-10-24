---
title: 'stores.lease'
description: 'Takes a lease on key for holder, lasting ttl_ms milliseconds (up to one hour); returns a fencing token.'
---

Part of [`stores`](/ref/stores/).

```luau
stores.lease(key: string, holder: string, ttl_ms: number) → number
```

Takes a lease on `key` for `holder`, lasting `ttl_ms` milliseconds (up to one hour); returns a fencing token.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `key` | `string` | yes |
| `holder` | `string` | yes |
| `ttl_ms` | `number` | yes |

## Returns

- `number`

## Used in

> "- `stores.lease(key, holder, ttl_ms)` returns a fencing token." — [Shared stores](/systems/shared-stores/)
