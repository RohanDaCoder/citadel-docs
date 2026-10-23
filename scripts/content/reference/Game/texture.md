---
title: "game.texture"
url: /docs/citadel/reference/Game/texture
---

# game.texture

Returns a new texture of width by height pixels, see-through until drawn on, for a pack's block or item.

```
game.texture(width: number, height: number) → Texture
```


## Parameters


## Returns


## Used in
- [`local side = game.texture(16, 16)`Custom blocks](/docs/citadel/custom-blocks)
- [`| `ui.image{}` | a picture | `image` (a `game.texture`), `color` (a tint) |`Layouts](/docs/citadel/layouts)
- [`pack, or a `game.texture`; `detail = 2` has four times the pixels. Or`Dialogs](/docs/citadel/dialogs)
- [`local ingot = game.texture(16, 16) -- a picture drawn in code, or a PNG file in the pack`Items](/docs/citadel/items)
- [`local t = game.texture(16, 16) -- see-through until drawn on`Items](/docs/citadel/items)
