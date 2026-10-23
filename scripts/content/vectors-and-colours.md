---
title: "Vectors and colours"
url: /docs/citadel/vectors-and-colours
---

# Vectors and colours

```luau
local a = vec3(1, 2, 3)
a + b, a - b, -a, a * 2, a * b, a / 2, a == b
a:magnitude(), a:unit(), a:dot(b), a:cross(b), a:distance(b), a:lerp(b, t), a:floor(), a:with{ y = 70 }
vec3.zero, vec3.up

local c = color(1, 0, 0.5)   -- or colors.red, color.hsv(0.6, 1, 1)
c * 0.5, c * d, c:lerp(d, t), c == d
color.gradient({ "gold", colors.white, "#3366ff" }, u)   -- the colour u (0..1) of the way along the list
color.gradient(list, u, true)                           -- a loop: u wraps, and the last colour runs back into the first
color.nearest(c)             -- the colour a screen or canvas really shows, since a picture snaps to the map palette

```
