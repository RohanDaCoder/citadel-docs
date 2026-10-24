---
title: "stores.renew"
description: "Extends the lease on key that token holds."
---

Part of [`stores`](/ref/stores/).

```luau
stores.renew(key: string, token: number)
```

Extends the lease on `key` that `token` holds.

## Parameters

| Name    | Type     | Required |
| ------- | -------- | -------- |
| `key`   | `string` | yes      |
| `token` | `number` | yes      |

## Used in

> "- `stores.renew(key, token)` and `stores.release(key, token)` maintain a lease." — [Shared stores](/systems/shared-stores/)
