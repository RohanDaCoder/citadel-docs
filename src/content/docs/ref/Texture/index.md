---
title: 'Texture type'
description: 'A picture drawn in code: game.texture(w, h)'
---

A picture drawn in code: `game.texture(w, h)`. Where a texture is taken, a string is a PNG file in the pack instead.

## Functions

| Call | Purpose |
| --- | --- |
| [`fill`](/ref/Texture/fill/) | Paints every pixel one colour. |
| [`pixel`](/ref/Texture/pixel/) | Sets one pixel; (0, 0) is the top left. |
| [`rect`](/ref/Texture/rect/) | Fills a rectangle of pixels. |
| [`frame`](/ref/Texture/frame/) | Draws a box's outline, one pixel wide. |
| [`noise`](/ref/Texture/noise/) | Paints each pixel in the area one of the colours at random, as for stone, bark or grain. |
| [`sprite`](/ref/Texture/sprite/) | Draws pixel art from rows of characters, each character painted with its ink, as on a screen. |
| [`draw`](/ref/Texture/draw/) | Draws another texture over this one; its see-through pixels are skipped. |
| [`copy`](/ref/Texture/copy/) | Returns a copy to draw on. |

## Fields

| Field | Purpose |
| --- | --- |
| [`texture.width: number`](/ref/Texture/width/) | Width in pixels. |
| [`texture.height: number`](/ref/Texture/height/) | Height in pixels. |
