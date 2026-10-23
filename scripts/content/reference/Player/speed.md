---
title: "player.speed"
url: /docs/citadel/reference/Player/speed
---

# player.speed

The body: what a pack sets on a player. See docs/luau-api.md, "Body and movement". Walk speed as a multiple of normal; 0 pins them.

```
player.speed: number
```


## Used in
- [`Numeric settings such as `player.speed`, `player.scale` and `player.reach``API basics](/docs/citadel/api-basics)
- [`player.speed = 2 -- walk speed as a multiple of normal; 0 pins them, 1 is normal`Body and movement](/docs/citadel/body-and-movement)
- [``player.speed = 0` for a cutscene. Do not use `gamemode = 3`.`Cameras](/docs/citadel/cameras)
- [`}, { easing = "in_out", on_done = function() player.camera = nil player.speed = 1 end })`Cameras](/docs/citadel/cameras)
