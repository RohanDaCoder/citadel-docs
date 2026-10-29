---
title: "durableStore:set"
url: /docs/citadel/reference/DurableStore/set
---

# durableStore:set

Writes a fact if its version is still `if_version`, and returns the new version. A mismatch errors with {err = "conflict"}.

```
durableStore:set(key: string, value: any, if_version: number, lease: number?) → number
```


## Parameters


## Returns
