---
title: "world.light_at"
description: "Block light and sky light, 0 to 15, and whether nothing above holds off the sky."
---

Part of [`world`](/ref/World/).

```luau
world.light_at(pos: Vec3) → (number, number, boolean)
```

Block light and sky light, 0 to 15, and whether nothing above holds off the sky.

## Parameters

| Name  | Type                 | Required |
| ----- | -------------------- | -------- |
| `pos` | [`Vec3`](/ref/Vec3/) | yes      |

## Returns

- `( number , number , boolean )`

## Used in

> "local block, sky, open = world.light_at(pos) -- block light 0..15, sky light 0..15, open sky" — [Zones and raycasts](/world/spatial-queries/)
> "- `world.light_at(pos)` gives three values: the block light, the sky light," — [Zones and raycasts](/world/spatial-queries/)
