---
title: "network.on_gone"
url: /docs/citadel/reference/network/on_gone
---

# network.on_gone

Called with the id of an instance that is gone.

```
network.on_gone(handler: (id: string) -> ()) → Connection
```


## Parameters


## Returns


## Used in
- [`network.on_gone(function(id) waiting[id] = nil end)`Network](/docs/citadel/network)
- [`- `network.on_gone(fn)` calls `fn(id)` when an instance is gone. It returns a connection.`Network](/docs/citadel/network)
