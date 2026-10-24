---
title: "world.block"
description: "The block there as the handle a hook gets: reads are live, and what it does lands on the next tick"
---

Part of [`world`](/ref/World/).

```luau
world.block(pos: Vec3) → BlockAt ?
```

The block there as the handle a hook gets: reads are live, and what it does lands on the next tick. `state` and `data` are for this pack's own blocks. `nil` where that chunk is not in memory.

## Parameters

| Name  | Type                 | Required |
| ----- | -------------------- | -------- |
| `pos` | [`Vec3`](/ref/Vec3/) | yes      |

## Returns

- [`BlockAt`](/ref/BlockAt/)

## Used in

> "world.block(pos) -- the block there as a handle: its state, its data, whether it is powered; see "power"" — [Blocks and terrain](/world/terrain-generation/)
> "it from anywhere with `world.block(pos)`:" — [Custom blocks](/world/custom-blocks/)
> "local door = world.block(vec3(10, 65, 10)) -- the block there, or nil where the chunk is not loaded" — [Custom blocks](/world/custom-blocks/)
