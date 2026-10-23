---
title: "ui.define"
url: /docs/citadel/reference/Ui/define
---

# ui.define

A layout of one child, centred over the hotbar with its bottom edge `margin` pixels above the screen's (40, or 25 when `hide_hud` takes the hearts and the food away). While the pack loads only.

```
ui.define(name: string, opts: { anchor: "bottom"?, margin: number?, [number]: LayoutNode }) → Layout
```


## Parameters


## Returns


## Used in
- [`local STATUS = ui.define("status", { anchor = "bottom", margin = 42,`Layouts](/docs/citadel/layouts)
- [`- `ui.define(name, { anchor, margin, child })` takes one child. `anchor` is`Layouts](/docs/citadel/layouts)
