---
title: 'hub.experiences'
description: 'The portals of the experience grounds'
---

Part of [`hub`](/ref/hub/).

```luau
hub.experiences() → { {slot: number, experience: string, title: string, pitch: string ?, icon: string ?, banner: string ?, players: number ?} }
```

The portals of the experience grounds. `experience` is what `/play` takes.

## Returns

- `{ {slot: number , experience: string , title: string , pitch: string ?, icon: string ?, banner: string ?, players: number ?} }`

## Used in

> "for _, e in hub.experiences() do print(e.slot, e.experience) end" — [Hub](/systems/hub/)
> "- `hub.experiences()` returns a list of `{slot, experience, title, pitch, icon, banner, players}`. `experience` is the name `/play` takes. A slot that is not in the list has no experience." — [Hub](/systems/hub/)
