---
title: "world.canvas"
url: /docs/citadel/reference/World/canvas
---

# world.canvas

Makes a picture of `width` by `height` maps (1 by 1 by default, 16 at most a side) with no frame of its own, for a frame, a hand or a screen.

```
world.canvas(opts: { width: number?, height: number? }?) → Canvas
```


## Parameters


## Returns


## Used in
- [`local c = world.canvas{} -- one map; world.canvas{ width = 4, height = 2 } is 4 by 2 maps (16 at most a side)`Canvases](/docs/citadel/canvases)
- [`item = "paper", -- canonical item name; or canvas = c, a world.canvas{}: a filled map of the picture`Displays](/docs/citadel/displays)
