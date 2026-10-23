---
title: "ui.box"
url: /docs/citadel/reference/Ui/box
---

# ui.box

The pieces of a layout (see "Layouts"). Sizes are pixels of the game's own HUD; a box is 1 to 256 a side. An item with an `id` is live.

```
ui.box(opts: { id: string?, width: number, height: number, color: Ink?, radius: number? }) → LayoutNode
```


## Parameters


## Returns


## Used in
- [`ui.box{ width = 82, height = 9, color = "#1c1410", radius = 2 }, -- the frame`Layouts](/docs/citadel/layouts)
- [`ui.box{ id = "hp", width = 80, height = 7, color = "red", radius = 1 },`Layouts](/docs/citadel/layouts)
