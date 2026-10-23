---
title: 'stores.request'
description: 'Sends one raw query to the store and yields until it answers; returns the answer table and any blob bytes.'
---

Part of [`stores`](/ref/stores/).

```luau
stores.request(query: {[string]: any }, bytes: string ?) → ({[string]: any }, string ?)
```

Sends one raw query to the store and yields until it answers; returns the answer table and any blob bytes.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `query` | `{[ string ]: any }` | yes |
| `bytes` | `string` | no |

## Returns

- `({[ string ]: any }, string ?)`
