---
title: "stores.lease"
url: /docs/citadel/reference/stores/lease
---

# stores.lease

Takes a lease on `key` for `holder`, lasting `ttl_ms` milliseconds (up to one hour); returns a fencing token.

```
stores.lease(key: string, holder: string, ttl_ms: number) → number
```


## Parameters


## Returns


## Used in
- [`- `stores.lease(key, holder, ttl_ms)` returns a fencing token.`Shared stores](/docs/citadel/shared-stores)
