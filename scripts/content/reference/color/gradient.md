---
title: "color.gradient"
url: /docs/citadel/reference/color/gradient
---

# color.gradient

The colour `u` (0 to 1) of the way along the list; with `loop`, `u` wraps and the last colour runs back into the first.

```
color.gradient(list: { Ink }, u: number, loop: boolean?) → Color
```


## Parameters


## Returns


## Used in
- [`color.gradient({ "gold", colors.white, "#3366ff" }, u) -- the colour u (0..1) of the way along the list`Vectors and colours](/docs/citadel/vectors-and-colours)
- [`color.gradient(list, u, true) -- a loop: u wraps, and the last colour runs back into the first`Vectors and colours](/docs/citadel/vectors-and-colours)
- [`function(_, i, n, t) return { color = color.gradient(list, (i - 1) / n - t * speed, true) } end`Text formatting](/docs/citadel/text-formatting)
