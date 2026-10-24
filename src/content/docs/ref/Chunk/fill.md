---
title: 'chunk:fill'
description: 'Fills a box of blocks, clipped to the chunk.'
---

Part of [`Chunk`](/ref/Chunk/).

```luau
chunk:fill(from: Vec3, to: Vec3, block: string)
```

Fills a box of blocks, clipped to the chunk.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `from` | [`Vec3`](/ref/Vec3/) | yes |
| `to` | [`Vec3`](/ref/Vec3/) | yes |
| `block` | `string` | yes |

## Used in

> "chunk:fill(" — [Guide: Your first pack](/getting-started/quick-start/)
> "`chunk:fill` fills the box between two corners, including both corners." — [Guide: Your first pack](/getting-started/quick-start/)
> "chunk:fill(vec3(-3, 64, -3), vec3(3, 64, 3), "quartz_block") -- clipped to the chunk" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
> "`chunk:fill` with corners outside the chunk is clipped to it, so one line" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
> "chunk:fill(vec3(chunk.min.x, 63, chunk.min.z), vec3(chunk.max.x, 63, chunk.max.z), "dirt")" — [Guide: Build a cottage](/guides/guide-build-a-cottage/)
> "chunk:fill(vec3(chunk.min.x, 64, chunk.min.z), vec3(chunk.max.x, 64, chunk.max.z), "grass_block")" — [Guide: Build a cottage](/guides/guide-build-a-cottage/)
