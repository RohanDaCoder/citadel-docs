---
title: "chunk:get"
description: "Chunk X coordinate (16 blocks each)"
---

Part of [`Chunk`](/ref/Chunk/).

```luau
chunk:get(pos: Vec3) → string
```

Chunk X coordinate (16 blocks each). Chunk Z coordinate (16 blocks each). The chunk's lowest corner, inclusive; y runs 0..255 or the game version's height. The chunk's highest corner, inclusive. Returns the block there now, by name; air outside the chunk.

## Parameters

| Name  | Type                 | Required |
| ----- | -------------------- | -------- |
| `pos` | [`Vec3`](/ref/Vec3/) | yes      |

## Returns

- `string`

## Used in

> "-- chunk:get(pos) what is there now, by name; air outside the chunk" — [Blocks and terrain](/world/terrain-generation/)
> "(not loaded), not `"air"`. Inside `on_generate`, `chunk:get` always works." — [Blocks and terrain](/world/terrain-generation/)
