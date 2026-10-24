---
title: "player.spawn_point"
description: "The player's own respawn point (the block of the position), or nil for the room's"
---

Part of [`player`](/ref/Player/).

```luau
player.spawn_point: Vec3 ?
```

The player's own respawn point (the block of the position), or nil for the room's. Writable; a point a pack sets needs no bed. nil clears it, a bed's point too.

## Used in

> "player.spawn_point = vec3(20.5, 65, -7.5) -- this player respawns here" — [Rooms](/concepts/rooms-and-dimensions/)
> "print(player.spawn_point) -- vec3, or nil for the room's point" — [Rooms](/concepts/rooms-and-dimensions/)
