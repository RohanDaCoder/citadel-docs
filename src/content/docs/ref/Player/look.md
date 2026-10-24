---
title: "player:look"
description: "Returns the unit vector the player faces."
---

Part of [`Player`](/ref/Player/).

```luau
player:look() → Vec3
```

Returns the unit vector the player faces.

## Returns

- [`Vec3`](/ref/Vec3/)

## Used in

> "player:look() -> vec3 -- unit vector the player faces" — [Input](/players/movement/)
> "world.raycast(player.at + vec3(0, 1.62, 0), player:look()) -- what the player is looking at" — [Zones and raycasts](/world/spatial-queries/)
> "hit.player:push(player:look() * 0.5 + vec3(0, 0.3, 0))" — [Room rules](/world/world-state/)
