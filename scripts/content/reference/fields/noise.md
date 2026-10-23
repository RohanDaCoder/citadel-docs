---
title: "fields.noise"
url: /docs/citadel/reference/fields/noise
---

# fields.noise

Smooth noise, about -1..1. `solid = true` changes with y too.

```
fields.noise(opts: { seed: number?, scale: number?, octaves: number?, gain: number?, lacunarity: number?, solid: boolean? }?) → Field
```


## Parameters


## Returns


## Used in
- [`local hills = fields.noise { seed = 7, scale = 96, octaves = 4 }`Blocks and terrain](/docs/citadel/blocks-and-terrain)
- [`local dry = fields.noise { seed = 8, scale = 300 }:gt(0)`Blocks and terrain](/docs/citadel/blocks-and-terrain)
