---
title: "stores.blob_list"
url: /docs/citadel/reference/stores/blob_list
---

# stores.blob_list

Lists a player's blobs across all blob stores in this scope, each with its store, key, version and size.

```
stores.blob_list(owner: string) → {{store: string, key: string, version: number, size: number}}
```


## Parameters


## Returns


## Used in
- [`- `stores.blob_list(player_uuid)` returns entries across all blob stores in this scope.`Shared stores](/docs/citadel/shared-stores)
