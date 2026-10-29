---
title: "network.status"
url: /docs/citadel/reference/network/status
---

# network.status

Says where this instance is. At most one a second is sent: the first at once, then the last of those that came after.

```
network.status(options: {open: number, status: string?, meta: any})
```


## Parameters


## Used in
- [`if me and me.id then network.status{ open = math.max(0, me.slots - #players.list()), status = "waiting" } end`Network](/docs/citadel/network)
- [`-- When the round starts: network.status{ open = 0, status = "playing" }`Network](/docs/citadel/network)
