---
title: 'chunk:set'
description: 'Sets one block; positions outside the chunk are ignored.'
---

Part of [`Chunk`](/ref/Chunk/).

```luau
chunk:set(pos: Vec3, block: string)
```

Sets one block; positions outside the chunk are ignored.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `pos` | [`Vec3`](/ref/Vec3/) | yes |
| `block` | `string` | yes |

## Used in

> "chunk:set(vec3(0, 64, 0), "gold_block")" — [Guide: Your first pack](/getting-started/quick-start/)
> "`chunk:set` replaces one floor block with gold. It ignores coordinates" — [Guide: Your first pack](/getting-started/quick-start/)
> "chunk:set(vec3(x, 64, z), "grass_block")" — [Guide: Coin rush](/guides/guide-coin-rush/)
> "chunk:set(vec3(x, 64, z), "stone_bricks")" — [Guide: Coin rush](/guides/guide-coin-rush/)
> "chunk:set(b.at, b.block) -- a block outside this chunk is ignored" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
> "that was made above. `chunk:set` ignores a block outside the chunk, so the" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
