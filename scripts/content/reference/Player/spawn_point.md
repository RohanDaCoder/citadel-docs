---
title: "player.spawn_point"
url: /docs/citadel/reference/Player/spawn_point
---

# player.spawn_point

The player's own respawn point (the block of the position), or nil for the room's. Writable; a point a pack sets needs no bed. nil clears it, a bed's point too.

```
player.spawn_point: Vec3?
```


## Used in
- [`player.spawn_point = vec3(20.5, 65, -7.5) -- this player respawns here`Rooms](/docs/citadel/rooms)
- [`print(player.spawn_point) -- vec3, or nil for the room's point`Rooms](/docs/citadel/rooms)
