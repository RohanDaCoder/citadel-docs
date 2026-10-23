---
title: "network.find"
url: /docs/citadel/reference/network/find
---

# network.find

The instance to send `players` players to (1 unless set), or nil when none has room. With `start`, one is started when none has room.

```
network.find(options: {label: string, players: number?, party: (Player | string)?, start: {member: string, slots: number, data: any}?}) → (NetworkStarted?, string?)
```


## Parameters


## Returns


## Used in
- [`local arena, why = network.find{`Network](/docs/citadel/network)
- [`- `network.find{ label, players?, party?, start? }` returns `{id, state}` for the instance to send `players` players to, or nil when no instance has room.`Network](/docs/citadel/network)
