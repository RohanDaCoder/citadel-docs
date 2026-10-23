---
title: "world.screen"
url: /docs/citadel/reference/World/screen
---

# world.screen

Puts a wall of map frames, `width` by `height` frames (128 pixels each), in front of a wall; `at` is the top-left frame. Returns a Screen.

```
world.screen(opts: { at: Vec3, facing: Facing | "up", up: Facing?, width: number?, height: number?, glow: boolean?, on_click: ((player: Player, x: number, y: number, button: "left" | "right") -> ())?, }) → Screen
```


## Parameters


## Returns


## Used in
- [`local board = world.screen{ at = vec3(-2, 68, -10), facing = "south", width = 4, height = 2 }`Scoreboard with a button](/docs/citadel/scoreboard-with-a-button)
- [`local board = world.screen{ at = vec3(-2, 68, -10), facing = "south", width = 4, height = 2 }`Screens](/docs/citadel/screens)
- [`Set `on_click` (in `world.screen{}` or later) to get the pixel a player`Screens](/docs/citadel/screens)
- [`local tv = world.screen{ at = vec3(-2, 70, -9), facing = "south", width = 4, height = 2 }`Canvases](/docs/citadel/canvases)
