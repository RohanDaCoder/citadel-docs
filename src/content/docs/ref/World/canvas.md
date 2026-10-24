---
title: "world.canvas"
description: "Makes a picture of width by height maps (1 by 1 by default, 16 at most a side) with no frame of its own, for a frame, a hand or a screen."
---

Part of [`world`](/ref/World/).

```luau
world.canvas(opts: { width: number ?, height: number ? }?) → Canvas
```

Makes a picture of `width` by `height` maps (1 by 1 by default, 16 at most a side) with no frame of its own, for a frame, a hand or a screen.

## Parameters

| Name   | Type                                    | Required |
| ------ | --------------------------------------- | -------- |
| `opts` | `{ width: number ?, height: number ? }` | no       |

## Returns

- [`Canvas`](/ref/Canvas/)

## Used in

> "local c = world.canvas{} -- one map; world.canvas{ width = 4, height = 2 } is 4 by 2 maps (16 at most a side)" — [Canvases](/ui/canvases/)
> "item = "paper", -- canonical item name; or canvas = c, a world.canvas{}: a filled map of the picture" — [Displays](/ui/displays/)
