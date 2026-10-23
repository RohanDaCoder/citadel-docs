---
title: 'ui.box'
description: 'The pieces of a layout (see "Layouts")'
---

Part of [`ui`](/ref/Ui/).

```luau
ui.box(opts: { id: string ?, width: number, height: number, color: Ink ?, radius: number ? }) → LayoutNode
```

The pieces of a layout (see "Layouts"). Sizes are pixels of the game's own HUD; a box is 1 to 256 a side. An item with an `id` is live.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `opts` | `{ id: string ?, width: number , height: number , color: Ink ?, radius: number ? }` | yes |

## Returns

- [`LayoutNode`](/ref/LayoutNode/)

## Used in

> "ui.box{ width = 82, height = 9, color = "#1c1410", radius = 2 },   -- the frame" — [Layouts](/ui/screens/)
> "ui.box{ id = "hp", width = 80, height = 7, color = "red", radius = 1 }," — [Layouts](/ui/screens/)
