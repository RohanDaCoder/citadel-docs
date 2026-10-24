---
title: "player:sound"
description: "Plays a sound by name to this player only, with an optional position, volume, pitch and category."
---

Part of [`Player`](/ref/Player/).

```luau
player:sound(name: string, opts: { at: Vec3 ?, volume: number ?, pitch: number ?, category: string ?, }?)
```

Plays a sound by name to this player only, with an optional position, volume, pitch and category.

## Parameters

| Name   | Type                                                                     | Required |
| ------ | ------------------------------------------------------------------------ | -------- |
| `name` | `string`                                                                 | yes      |
| `opts` | `{ at: Vec3 ?, volume: number ?, pitch: number ?, category: string ?, }` | no       |

## Used in

> "player:sound(name, { at = player.at, volume = 1, pitch = 1, category = "record" })" — [Players](/players/player-lifecycle/)
