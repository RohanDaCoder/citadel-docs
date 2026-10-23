---
title: 'stores.blob_list'
description: 'Lists a player''s blobs across all blob stores in this scope, each with its store, key, version and size.'
---

Part of [`stores`](/ref/stores/).

```luau
stores.blob_list(owner: string) → {{store: string, key: string, version: number, size: number }}
```

Lists a player's blobs across all blob stores in this scope, each with its store, key, version and size.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `owner` | `string` | yes |

## Returns

- `{{store: string , key: string , version: number , size: number }}`

## Used in

> "- `stores.blob_list(player_uuid)` returns entries across all blob stores in this scope." — [Shared stores](/systems/shared-stores/)
