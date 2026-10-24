---
title: "world.zone"
description: "Makes a box of blocks, both corners included, that knows who is in it; checked once a tick by feet position"
---

Part of [`world`](/ref/World/).

```luau
world.zone(opts: { from: Vec3, to: Vec3, on_enter: ((player: Player) -> ())?, on_leave: ((player: Player) -> ())? }) → Zone
```

Makes a box of blocks, both corners included, that knows who is in it; checked once a tick by feet position. Ends with the script.

## Parameters

| Name   | Type                                                                                                     | Required |
| ------ | -------------------------------------------------------------------------------------------------------- | -------- |
| `opts` | `{ from: Vec3 , to: Vec3 , on_enter: ((player: Player ) -> ())?, on_leave: ((player: Player ) -> ())? }` | yes      |

## Returns

- [`Zone`](/ref/Zone/)

## Used in

> "coin.zone = world.zone{" — [Guide: Coin rush](/guides/guide-coin-rush/)
> "- `world.zone` is a box of blocks. Here it is one block, and `on_enter`" — [Guide: Coin rush](/guides/guide-coin-rush/)
> "room.world.zone{ from = from, to = to, on_enter = function(p)" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
> "room.world.zone{ from = vec3(-40, 30, -10), to = vec3(40, 58, c.finish.z + 10), on_enter = function(p)" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
> "local goal = world.zone{ from = vec3(10, 64, 10), to = vec3(14, 66, 14)," — [Zones and raycasts](/world/spatial-queries/)
