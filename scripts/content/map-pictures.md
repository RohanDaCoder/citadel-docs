---
title: "Map pictures"
url: /docs/citadel/map-pictures
---

# Map pictures

- The frame hangs in the block `at`, on the side `facing`.
- `"up"` lies flat on a floor (1.13 and later). A wall side works from 1.8.
- The frame does not turn or move.
- Set `canvas` to change the picture. `destroy` removes the frame.
```luau
local card = world.display{ kind = "frame", at = vec3(3, 65, 7), facing = "up", canvas = deck[12], invisible = true }
card.canvas = deck[53]        -- the back
card.id; card:destroy()

```
A canvas or screen pixel painted `colors.transparent` is see-through. `clear(colors.transparent)` empties a canvas.
