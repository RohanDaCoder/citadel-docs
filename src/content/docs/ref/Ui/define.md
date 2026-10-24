---
title: 'ui.define'
description: 'A layout of one child, centred over the hotbar with its bottom edge margin pixels above the screen''s (40, or 25 when hide_hud takes the hearts and the food away)'
---

Part of [`ui`](/ref/Ui/).

```luau
ui.define(name: string, opts: { anchor: "bottom" ?, margin: number ?, [number]: LayoutNode }) → Layout
```

A layout of one child, centred over the hotbar with its bottom edge `margin` pixels above the screen's (40, or 25 when `hide_hud` takes the hearts and the food away). While the pack loads only.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `name` | `string` | yes |
| `opts` | `{ anchor: "bottom" ?, margin: number ?, [ number ]: LayoutNode }` | yes |

## Returns

- [`Layout`](/ref/Layout/)

## Used in

> "local STATUS = ui.define("status", { anchor = "bottom", margin = 42," — [Layouts](/ui/screens/)
> "- `ui.define(name, { anchor, margin, child })` takes one child. `anchor` is" — [Layouts](/ui/screens/)
