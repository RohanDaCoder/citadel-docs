---
title: 'hub.hubs'
description: 'Every hub that is online, this one included'
---

Part of [`hub`](/ref/hub/).

```luau
hub.hubs() → { {id: string, name: string, players: number ?, region: string ?} }
```

Every hub that is online, this one included. `id` is what `player:connect` takes.

## Returns

- `{ {id: string , name: string , players: number ?, region: string ?} }`

## Used in

> "for _, h in hub.hubs() do print(h.name, h.players) end" — [Hub](/systems/hub/)
> "- `hub.hubs()` returns a list of `{id, name, players, region}`, one per hub that is online, this one included. `player:connect(id)` sends a player to that hub." — [Hub](/systems/hub/)
