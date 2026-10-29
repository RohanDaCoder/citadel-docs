---
title: "world.block"
url: /docs/citadel/reference/World/block
---

# world.block

The block there as the handle a hook gets: reads are live, and what it does lands on the next tick. `state` and `data` are for this pack's own blocks. `nil` where that chunk is not in memory.

```
world.block(pos: Vec3) → BlockAt?
```


## Parameters


## Returns


## Used in
- [`world.block(pos) -- the block there as a handle: its state, its data, whether it is powered; see "power"`Blocks and terrain](/docs/citadel/blocks-and-terrain)
- [`it from anywhere with `world.block(pos)`:`Custom blocks](/docs/citadel/custom-blocks)
- [`local door = world.block(vec3(10, 65, 10)) -- the block there, or nil where the chunk is not loaded`Custom blocks](/docs/citadel/custom-blocks)
