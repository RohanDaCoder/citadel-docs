---
title: "ModelBuild type"
description: "What models.new hands its build function: makes the model's materials, textures, parts and animations."
---

What `models.new` hands its build function: makes the model's materials, textures, parts and animations.

## Functions

| Call                                      | Purpose                                                                                                                                                                                                          |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`material`](/ref/ModelBuild/material/)   | Makes a named colour a display may repaint; `grain` (0 to 1) darkens pixels into four tones, `alpha` below 1 is glass.                                                                                           |
| [`texture`](/ref/ModelBuild/texture/)     | Makes a pixel picture for one face; with `tint`, drawn in greys and coloured by that material. With `scroll`, it moves by itself on a block drawn from the model, `speed` texels a tick (1, 2, 3, or 0.5, 0.25). |
| [`part`](/ref/ModelBuild/part/)           | Makes a named child part of the root that turns around its `pivot`, the model's origin unless given.                                                                                                             |
| [`animation`](/ref/ModelBuild/animation/) | `{ length = seconds, loop = false, <part name> = { rotation = { [t] = is both named fields and part names, so this one is open.                                                                                  |
