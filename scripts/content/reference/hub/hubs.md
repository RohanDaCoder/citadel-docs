---
title: "hub.hubs"
url: /docs/citadel/reference/hub/hubs
---

# hub.hubs

Every hub that is online, this one included. `id` is what `player:connect` takes.

```
hub.hubs() → { {id: string, name: string, players: number?, region: string?} }
```


## Returns


## Used in
- [`for _, h in hub.hubs() do print(h.name, h.players) end`Hub](/docs/citadel/hub)
- [`- `hub.hubs()` returns a list of `{id, name, players, region}`, one per hub that is online, this one included. `player:connect(id)` sends a player to that hub.`Hub](/docs/citadel/hub)
