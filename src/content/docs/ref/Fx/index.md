---
title: 'fx global · type Fx'
description: 'Particles for a room: Minecraft''s particle packet; the fx global, or room.fx.'
---

Particles for a room: Minecraft's particle packet; the `fx` global, or `room.fx`.

Part of the [Sound](/ui/sound/) article.

## Functions

| Call | Purpose |
| --- | --- |
| [`particle`](/ref/Fx/particle/) | Shows particle `name` ("dust", "end_rod", "explosion", "firework", "flame", "note", "totem_of_undying") at `pos`, or at every point of a list. Each point reaches players in the room within 64 blocks of its origin in 3D, including the boundary, before spread or velocity. `count` (1) at each point in a box `spread` (0) out; or with `velocity`, one particle moving along it (`speed` 1 then, else 0). `color` and `size` are for dust only. |
