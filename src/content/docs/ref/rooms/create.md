---
title: 'rooms.create'
description: 'Creates an isolated room with its own chunks, players and effects; spawn_point defaults to (0.5, 65, 0.5), generate fills each chunk.'
---

Part of [`rooms`](/ref/rooms/).

```luau
rooms.create(opts: { spawn_point: Vec3 ?, generate: ((chunk: Chunk) -> ())? }) → Room
```

Creates an isolated room with its own chunks, players and effects; `spawn_point` defaults to (0.5, 65, 0.5), `generate` fills each chunk.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `opts` | `{ spawn_point: Vec3 ?, generate: ((chunk: Chunk ) -> ())? }` | yes |

## Returns

- [`Room`](/ref/Room/)

## Used in

> "`rooms.create` makes a world with its own chunks, players and effects:" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
> "local room = rooms.create{" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
> "`rooms.create` gives a player their own world, with own chunks, players and" — [A world per player](/concepts/rooms-and-dimensions/)
> "local mine = rooms.create{" — [A world per player](/concepts/rooms-and-dimensions/)
> "- The first six belong to the main room. `rooms.create{}` gives another room" — [API basics](/concepts/conventions/)
> "- On a `mode: lite` world and in a room made by `rooms.create`, the rule is" — [Blocks and terrain](/world/terrain-generation/)
