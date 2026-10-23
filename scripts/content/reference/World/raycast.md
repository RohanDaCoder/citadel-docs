---
title: "world.raycast"
url: /docs/citadel/reference/World/raycast
---

# world.raycast

The first block a ray from `from` along `direction` meets within `max` blocks, and the face it came in through; nil for none.

```
world.raycast(from: Vec3, direction: Vec3, max: number?) → RayHit?
```


## Parameters


## Returns


## Used in
- [`world.raycast(from, direction, 32) -- the first block a ray meets within 32 blocks, or nil:`Zones and raycasts](/docs/citadel/zones-and-raycasts)
- [`world.raycast(player.at + vec3(0, 1.62, 0), player:look()) -- what the player is looking at`Zones and raycasts](/docs/citadel/zones-and-raycasts)
