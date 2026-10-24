---
title: "color.hsv"
description: "Makes a colour from hue, saturation and value, each 0 to 1."
---

Part of [`color`](/ref/color/).

```luau
color.hsv(h: number, s: number, v: number) → Color
```

Makes a colour from hue, saturation and value, each 0 to 1.

## Parameters

| Name | Type     | Required |
| ---- | -------- | -------- |
| `h`  | `number` | yes      |
| `s`  | `number` | yes      |
| `v`  | `number` | yes      |

## Returns

- [`Color`](/ref/Color/)

## Used in

> "`color.hsv(h, s, v)`, everywhere, text included." — [API basics](/concepts/conventions/)
> "local c = color(1, 0, 0.5) -- or colors.red, color.hsv(0.6, 1, 1)" — [Vectors and colours](/concepts/conventions/)
> "local rainbow = function(letter, i, n, t) return { color = color.hsv((i - 1) / n + t, 1, 1) } end" — [Text formatting](/ui/ui-basics/)
