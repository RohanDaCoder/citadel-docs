---
title: "color.nearest"
description: "The colour a picture really shows, since it snaps to the map palette."
---

Part of [`color`](/ref/color/).

```luau
color.nearest(c: Color) → Color
```

The colour a picture really shows, since it snaps to the map palette.

## Parameters

| Name | Type                   | Required |
| ---- | ---------------------- | -------- |
| `c`  | [`Color`](/ref/Color/) | yes      |

## Returns

- [`Color`](/ref/Color/)

## Used in

> "color.nearest(c) -- the colour a screen or canvas really shows, since a picture snaps to the map palette" — [Vectors and colours](/concepts/conventions/)
> "- `color.nearest(c)` does that snap in advance." — [Screens](/ui/screens/)
