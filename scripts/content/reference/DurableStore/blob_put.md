---
title: "durableStore:blob_put"
url: /docs/citadel/reference/DurableStore/blob_put
---

# durableStore:blob_put

Writes a player's binary blob if its version is still `if_version`, and returns the new version. At most 32 MiB.

```
durableStore:blob_put(owner: string, key: string, bytes: string, if_version: number, lease: number?) → number
```


## Parameters


## Returns
