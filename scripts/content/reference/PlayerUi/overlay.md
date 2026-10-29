---
title: "playerUi.overlay"
url: /docs/citadel/reference/PlayerUi/overlay
---

# playerUi.overlay

Puts a canvas in a corner of this player's screen, `size` screen pixels square at GUI scale 1 (96 by default, 16 to 511), `margin` from the edges (4 by default); nil where `player:supports("overlay")` is false.

```
playerUi.overlay(opts: { corner: ("top_left" | "top_right" | "bottom_left" | "bottom_right")?, size: number?, margin: number? }?) → Overlay?
```


## Parameters


## Returns
