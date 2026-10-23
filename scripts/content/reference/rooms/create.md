---
title: "rooms.create"
url: /docs/citadel/reference/rooms/create
---

# rooms.create

Creates an isolated room with its own chunks, players and effects; `spawn_point` defaults to (0.5, 65, 0.5), `generate` fills each chunk.

```
rooms.create(opts: { spawn_point: Vec3?, generate: ((chunk: Chunk) -> ())? }) → Room
```


## Parameters


## Returns


## Used in
- [``rooms.create` makes a world with its own chunks, players and effects:`Guide: Parkour, a room each](/docs/citadel/guides/parkour-a-room-each)
- [`local room = rooms.create{`Guide: Parkour, a room each](/docs/citadel/guides/parkour-a-room-each)
- [``rooms.create` gives a player their own world, with own chunks, players and`A world per player](/docs/citadel/a-world-per-player)
- [`local mine = rooms.create{`A world per player](/docs/citadel/a-world-per-player)
- [`- The first six belong to the main room. `rooms.create{}` gives another room`API basics](/docs/citadel/api-basics)
- [`- On a `mode: lite` world and in a room made by `rooms.create`, the rule is`Blocks and terrain](/docs/citadel/blocks-and-terrain)
- [``game` describes this room's game version. `rooms.create` inherits the`Game data](/docs/citadel/game-data)
- [``rooms.create`. It is on on a `mode: full` world and after`Game data](/docs/citadel/game-data)
