---
title: "stores.release"
description: "Gives up the lease on key that token holds."
---

Part of [`stores`](/ref/stores/).

```luau
stores.release(key: string, token: number)
```

Gives up the lease on `key` that `token` holds.

## Parameters

| Name    | Type     | Required |
| ------- | -------- | -------- |
| `key`   | `string` | yes      |
| `token` | `number` | yes      |

## Used in

> "- `stores.renew(key, token)` and `stores.release(key, token)` maintain a lease." — [Shared stores](/systems/shared-stores/)
