---
title: "world.raycasts"
url: /docs/citadel/reference/World/raycasts
---

# world.raycasts

`n` lines at once. `rays` holds six f64 a line (from x, y, z, to x, y, z); `out` gets one f64 a line: how far along it the first block is that stops it, or -1 for a clear line.

```
world.raycasts(rays: buffer, out: buffer, n: number)
```


## Parameters


## Used in
- [`world.raycasts(rays, out, n) -- n lines at once, in buffers; see below`Zones and raycasts](/docs/citadel/zones-and-raycasts)
- [`- `world.sees` and `world.raycasts` look as a mob looks: a block with a`Zones and raycasts](/docs/citadel/zones-and-raycasts)
