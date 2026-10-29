---
title: "fx.particle"
url: /docs/citadel/reference/Fx/particle
---

# fx.particle

Shows particle `name` ("dust", "end_rod", "explosion", "firework", "flame", "note", "totem_of_undying") at `pos`, or at every point of a list. Each point reaches players in the room within 64 blocks of its origin in 3D, including the boundary, before spread or velocity. `count` (1) at each point in a box `spread` (0) out; or with `velocity`, one particle moving along it (`speed` 1 then, else 0). `color` and `size` are for dust only.

```
fx.particle(name: string, pos: Vec3 | { Vec3 }, opts: { count: number?, spread: (number | Vec3)?, velocity: Vec3?, speed: number?, color: Ink?, size: number?, }?)
```


## Parameters


## Used in
- [`fx.particle("totem_of_undying", at + vec3(0.5, 0.5, 0.5), { count = 12, spread = 0.4, speed = 0.3 })`Guide: Coin rush](/docs/citadel/guides/coin-rush)
- [`fx.particle("firework", arena.CENTER + vec3(0, 2, 0), { count = 60, spread = 2, speed = 0.1 })`Guide: Coin rush](/docs/citadel/guides/coin-rush)
- [`room.fx.particle("firework", c.finish + vec3(0.5, 2, 0.5), { count = 50, spread = 1.5, speed = 0.1 })`Guide: Parkour, a room each](/docs/citadel/guides/parkour-a-room-each)
- [`room.fx.particle("firework", c.finish + vec3(0.5, 2, 0.5), { count = 50, spread = 1.5, speed = 0.1 })`Guide: Parkour, a room each](/docs/citadel/guides/parkour-a-room-each)
- [`fx.particle(name, pos, { count = 1, spread = 0, velocity = nil, speed = 0, color = nil, size = 1 })`Particles and lasers](/docs/citadel/particles-and-lasers)
- [`fx.particle("dust", points, { color = colors.red, size = 1.5 })`Particles and lasers](/docs/citadel/particles-and-lasers)
