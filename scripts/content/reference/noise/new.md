---
title: "noise.new"
url: /docs/citadel/reference/noise/new
---

# noise.new

Returns a noise. `scale` is the size of a hill in blocks (64), and each of the `octaves` (1) adds detail `lacunarity` (2) times finer and `gain` (0.5) times as strong.

```
noise.new(opts: { seed: number?, scale: number?, octaves: number?, gain: number?, lacunarity: number? }?) → Noise
```


## Parameters


## Returns


## Used in
- [`local hills = noise.new { seed = 7, scale = 96, octaves = 4 }`Blocks and terrain](/docs/citadel/blocks-and-terrain)
- [`local hills = noise.new { seed = 7, scale = 96, octaves = 4 }`Blocks and terrain](/docs/citadel/blocks-and-terrain)
