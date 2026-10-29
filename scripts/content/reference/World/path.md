---
title: "world.path"
url: /docs/citadel/reference/World/path
---

# world.path

The points a body walks from `from` to the block at `to`, or nil. The game's own search: a step up of one block, falls of `fall` (3). `size` is { width, height } (0.6, 1.8); `swim` goes through water; `range` (the distance + 16) and `budget` (2000 nodes) stop a long search, which then gives the part that came closest.

```
world.path(from: Vec3, to: Vec3, opts: { size: (number | { number })?, swim: boolean?, fall: number?, range: number?, budget: number? }?) → { Vec3 }?
```


## Parameters


## Returns


## Used in
- [`need. It turns smoothly, follows the points of `world.path`, jumps when a`Custom entities](/docs/citadel/custom-entities)
- [`-- Body i of `b` walks the route { points = world.path(...), at = 1 }.`Custom entities](/docs/citadel/custom-entities)
- [`world.path(from, to, { size = { 0.6, 1.95 } }) -- the points a body walks, a list of vec3, or nil`Zones and raycasts](/docs/citadel/zones-and-raycasts)
- [`- `world.path(from, to, opts)` is the game's own search for a mob: four ways`Zones and raycasts](/docs/citadel/zones-and-raycasts)
