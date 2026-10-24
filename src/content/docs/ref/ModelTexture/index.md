---
title: "ModelTexture type"
description: "Pixel art for one face of a box: plain RGBA, and never repainted."
---

Pixel art for one face of a box: plain RGBA, and never repainted.

## Functions

| Call                                | Purpose                                                              |
| ----------------------------------- | -------------------------------------------------------------------- |
| [`fill`](/ref/ModelTexture/fill/)   | Paints every pixel one colour.                                       |
| [`pixel`](/ref/ModelTexture/pixel/) | Paints the pixel at x, y; `colors.transparent` makes it see-through. |
| [`rect`](/ref/ModelTexture/rect/)   | Paints a rectangle `w` by `h` pixels from x, y.                      |
