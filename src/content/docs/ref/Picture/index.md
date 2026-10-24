---
title: "Picture type"
description: "The calls a screen, a canvas and a view all share."
---

The calls a screen, a canvas and a view all share.

## Functions

| Call                                 | Purpose                                                                                                                                                                                      |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`clear`](/ref/Picture/clear/)       | Its width in pixels: 128 for each map across. Its height in pixels: 128 for each map down. Paints every pixel one colour; black by default. On a view, the default clears it to see-through. |
| [`set`](/ref/Picture/set/)           | Paints one pixel; (0, 0) is the top-left.                                                                                                                                                    |
| [`fill`](/ref/Picture/fill/)         | Fills a w by h box of pixels with one colour, its top-left at (x, y).                                                                                                                        |
| [`rect`](/ref/Picture/rect/)         | Fills a box like `fill`, with smoothed rounded corners of `radius` pixels when given.                                                                                                        |
| [`circle`](/ref/Picture/circle/)     | Fills a circle of radius `r` pixels around (x, y).                                                                                                                                           |
| [`text`](/ref/Picture/text/)         | Draws text in DejaVu Sans Bold, `size` pixels tall (16 by default), smoothed; returns its width in pixels.                                                                                   |
| [`measure`](/ref/Picture/measure/)   | The width in pixels that `text` would draw, without drawing it; for centring.                                                                                                                |
| [`line`](/ref/Picture/line/)         | Draws a smoothed line with round ends, `width` pixels wide (1 by default); positions may be fractions.                                                                                       |
| [`ring`](/ref/Picture/ring/)         | Draws a circle's outline, `width` pixels wide (1 by default), smoothed.                                                                                                                      |
| [`polygon`](/ref/Picture/polygon/)   | Fills a smoothed shape with any number of corners; a point is `{x, y}` or `{ x = .., y = .. }`.                                                                                              |
| [`gradient`](/ref/Picture/gradient/) | Fills a box that fades from `from` to `to`, top to bottom; `"across"` runs it left to right.                                                                                                 |
| [`sprite`](/ref/Picture/sprite/)     | Draws pixel art: each string a row, each character a dot `scale` pixels square (1 by default); a character with no ink is skipped.                                                           |
| [`pixels`](/ref/Picture/pixels/)     | Writes raw RGB bytes (a buffer or a string), three a pixel, row by row, into a w by h box.                                                                                                   |
| [`draw`](/ref/Picture/draw/)         | Draws another screen, canvas or view with its top-left at (x, y), skipping its transparent pixels.                                                                                           |
| [`part`](/ref/Picture/part/)         | One map of the picture, `{ id = .. }`, by column and row from (0, 0) top- left; for a hand or a single frame.                                                                                |
| [`play`](/ref/Picture/play/)         | Plays a raw RGB video file from the pack at `fps` 0.5 to 20, the engine drawing each frame; returns the Video.                                                                               |
