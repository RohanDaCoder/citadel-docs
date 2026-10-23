---
title: "room.spawn_point"
url: /docs/citadel/reference/Room/spawn_point
---

# room.spawn_point

The room's number. Rooms also compare by identity with `==`. Where players arrive in this room; writable. A write is not stored and does not move the chunks that stay loaded.

```
room.spawn_point: Vec3
```


## Used in
- [`room.spawn_point = vec3(0.5, 80, 0.5) -- the same field of a different room`Rooms](/docs/citadel/rooms)
- [`- A write to `world.spawn_point` or `room.spawn_point` changes where a player`Rooms](/docs/citadel/rooms)
