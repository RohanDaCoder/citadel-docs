---
title: "room.spawn_point"
description: "The room's number"
---

Part of [`room`](/ref/Room/).

```luau
room.spawn_point: Vec3
```

The room's number. Rooms also compare by identity with `==`. Where players arrive in this room; writable. A write is not stored and does not move the chunks that stay loaded.

## Used in

> "room.spawn_point = vec3(0.5, 80, 0.5) -- the same field of a different room" — [Rooms](/concepts/rooms-and-dimensions/)
> "- A write to `world.spawn_point` or `room.spawn_point` changes where a player" — [Rooms](/concepts/rooms-and-dimensions/)
