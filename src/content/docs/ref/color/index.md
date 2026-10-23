---
title: 'color global'
description: 'Colour helpers: hsv, gradients and nearest-map-colour.'
---

Colour helpers: hsv, gradients and nearest-map-colour.

`((r: number, g: number, b: number) -> Color)`

Part of the [Pack anatomy](/concepts/pack-anatomy/) article.

## Functions

| Call | Purpose |
| --- | --- |
| [`hsv`](/ref/color/hsv/) | Makes a colour from hue, saturation and value, each 0 to 1. |
| [`nearest`](/ref/color/nearest/) | The colour a picture really shows, since it snaps to the map palette. |
| [`gradient`](/ref/color/gradient/) | The colour `u` (0 to 1) of the way along the list; with `loop`, `u` wraps and the last colour runs back into the first. |
