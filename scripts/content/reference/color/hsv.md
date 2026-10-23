---
title: "color.hsv"
url: /docs/citadel/reference/color/hsv
---

# color.hsv

Makes a colour from hue, saturation and value, each 0 to 1.

```
color.hsv(h: number, s: number, v: number) → Color
```


## Parameters


## Returns


## Used in
- [``color.hsv(h, s, v)`, everywhere, text included.`API basics](/docs/citadel/api-basics)
- [`local c = color(1, 0, 0.5) -- or colors.red, color.hsv(0.6, 1, 1)`Vectors and colours](/docs/citadel/vectors-and-colours)
- [`local rainbow = function(letter, i, n, t) return { color = color.hsv((i - 1) / n + t, 1, 1) } end`Text formatting](/docs/citadel/text-formatting)
