---
title: "world.npc"
description: "Places a player-shaped entity every client from 1.8 sees; removed when the script ends or reloads."
---

Part of [`world`](/ref/World/).

```luau
world.npc(opts: { name: string ?, at: Vec3 ?, rotation: BodyRotation ?, skin: (string | { value: string, signature: string } | false)?, }) → Npc
```

Places a player-shaped entity every client from 1.8 sees; removed when the script ends or reloads.

## Parameters

| Name   | Type                                                                                                                             | Required |
| ------ | -------------------------------------------------------------------------------------------------------------------------------- | -------- |
| `opts` | `{ name: string ?, at: Vec3 ?, rotation: BodyRotation ?, skin: ( string \| { value: string , signature: string } \| false )?, }` | yes      |

## Returns

- [`Npc`](/ref/Npc/)

## Used in

> "`world.npc{ skin = }`. The signature is optional." — [Blocks and terrain](/world/terrain-generation/)
> "\| A player-shaped character with a skin and equipment \| `world.npc` \| Adds avatar-specific behavior. \|" — [Displays](/ui/displays/)
> "local n = world.npc{ name = "Dealer", at = vec3(0.5, 65, 4.5), rotation = { yaw = 180, pitch = 0 }," — [NPCs](/entities/npcs/)
