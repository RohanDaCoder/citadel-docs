---
title: "color.gradient"
description: "The colour u (0 to 1) of the way along the list; with loop, u wraps and the last colour runs back into the first."
---

Part of [`color`](/ref/color/).

```luau
color.gradient(list: { Ink }, u: number, loop: boolean ?) → Color
```

The colour `u` (0 to 1) of the way along the list; with `loop`, `u` wraps and the last colour runs back into the first.

## Parameters

| Name   | Type      | Required |
| ------ | --------- | -------- |
| `list` | `{ Ink }` | yes      |
| `u`    | `number`  | yes      |
| `loop` | `boolean` | no       |

## Returns

- [`Color`](/ref/Color/)

## Used in

> "color.gradient({ "gold", colors.white, "#3366ff" }, u) -- the colour u (0..1) of the way along the list" — [Vectors and colours](/concepts/conventions/)
> "color.gradient(list, u, true) -- a loop: u wraps, and the last colour runs back into the first" — [Vectors and colours](/concepts/conventions/)
> "function(_, i, n, t) return { color = color.gradient(list, (i - 1) / n - t * speed, true) } end" — [Text formatting](/ui/ui-basics/)
