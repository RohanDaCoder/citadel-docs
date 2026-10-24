---
title: 'hub.servers'
description: 'The players'' servers that are online, and the published experiences (category == "experience")'
---

Part of [`hub`](/ref/hub/).

```luau
hub.servers() → { {id: string, name: string, category: string, motd: string ?, icon: string ?, banner: string ?, players: number ?, maxPlayers: number ?} }
```

The players' servers that are online, and the published experiences (`category == "experience"`). `id` is what `player:connect` takes.

## Returns

- `{ {id: string , name: string , category: string , motd: string ?, icon: string ?, banner: string ?, players: number ?, maxPlayers: number ?} }`

## Used in

> "for _, s in hub.servers() do print(s.name, s.players) end" — [Hub](/systems/hub/)
> "- `hub.servers()` returns a list of `{id, name, category, motd, icon, banner, players, maxPlayers}`. `id` is what `player:connect` takes. A field Minefort does not know is nil. An entry with `category = "experience"` is a published experience: its `id` is the name `/play` takes, `motd` its pitch, and `banner` the URL of its banner, or nil." — [Hub](/systems/hub/)
