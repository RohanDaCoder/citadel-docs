---
title: "citadel.on_slow"
url: /docs/citadel/reference/citadel/on_slow
---

# citadel.on_slow

Called when a batch runs out of budget; at most once a second.

```
citadel.on_slow(fn: (slow: Slow) -> ()) → Connection
```


## Parameters


## Returns


## Used in
- [`citadel.on_slow(function(slow) end) -- a batch that ran out of budget; see "Limits and reload"`Version info](/docs/citadel/version-info)
- [`citadel.on_slow(function(slow)`Limits and reload](/docs/citadel/limits-and-reload)
