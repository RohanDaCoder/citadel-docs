---
title: "chunk:set_biome"
description: 'Sets the biome of one column: a vanilla name ("desert") or the name game.biomes.define returned.'
---

Part of [`Chunk`](/ref/Chunk/).

```luau
chunk:set_biome(pos: Vec3, biome: string)
```

Sets the biome of one column: a vanilla name ("desert") or the name `game.biomes.define` returned.

## Parameters

| Name    | Type                 | Required |
| ------- | -------------------- | -------- |
| `pos`   | [`Vec3`](/ref/Vec3/) | yes      |
| `biome` | `string`             | yes      |

## Used in

> "-- chunk:set_biome(pos, biome) the biome of one column; see "biomes"" — [Blocks and terrain](/world/terrain-generation/)
> "chunk:set_biome(pos, "desert") -- one column; pos.y is not read" — [Blocks and terrain](/world/terrain-generation/)
