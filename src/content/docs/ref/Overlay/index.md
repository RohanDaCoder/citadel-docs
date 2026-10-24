---
title: 'Overlay type'
description: 'A canvas on one player''s screen, from player.ui.overlay: 128 by 128, drawn like a canvas'
---

A canvas on one player's screen, from `player.ui.overlay`: 128 by 128, drawn like a canvas. Row 0 is the engine's and never shows; draw in rows 1 to 127. Colour `colors.transparent` shows the game through it.

[`Picture`](/ref/Picture/)

## Functions

| Call | Purpose |
| --- | --- |
| [`destroy`](/ref/Overlay/destroy/) | Takes it off the player's screen. |

## Fields

| Field | Purpose |
| --- | --- |
| [`overlay.open: boolean`](/ref/Overlay/open/) | True until `destroy` or the player leaves. |
