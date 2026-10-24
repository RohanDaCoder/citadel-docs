---
title: "game.texture"
description: "Returns a new texture of width by height pixels, see-through until drawn on, for a pack's block or item."
---

Part of [`game`](/ref/Game/).

```luau
game.texture(width: number, height: number) → Texture
```

Returns a new texture of width by height pixels, see-through until drawn on, for a pack's block or item.

## Parameters

| Name     | Type     | Required |
| -------- | -------- | -------- |
| `width`  | `number` | yes      |
| `height` | `number` | yes      |

## Returns

- [`Texture`](/ref/Texture/)

## Used in

> "local side = game.texture(16, 16)" — [Custom blocks](/world/custom-blocks/)
> "\| `ui.image{}` \| a picture \| `image` (a `game.texture`), `color` (a tint) \|" — [Layouts](/ui/screens/)
> "pack, or a `game.texture`; `detail = 2` has four times the pixels. Or" — [Dialogs](/ui/dialogs/)
> "local ingot = game.texture(16, 16) -- a picture drawn in code, or a PNG file in the pack" — [Items](/players/inventory/)
> "local t = game.texture(16, 16) -- see-through until drawn on" — [Items](/players/inventory/)
