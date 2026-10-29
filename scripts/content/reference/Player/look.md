---
title: "player:look"
url: /docs/citadel/reference/Player/look
---

# player:look

Returns the unit vector the player faces.

```
player:look() → Vec3
```


## Returns


## Used in
- [`player:look() -> vec3 -- unit vector the player faces`Input](/docs/citadel/input)
- [`world.raycast(player.at + vec3(0, 1.62, 0), player:look()) -- what the player is looking at`Zones and raycasts](/docs/citadel/zones-and-raycasts)
- [`hit.player:push(player:look() * 0.5 + vec3(0, 0.3, 0))`Room rules](/docs/citadel/room-rules)
