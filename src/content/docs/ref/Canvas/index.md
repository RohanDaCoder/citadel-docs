---
title: "Canvas type"
description: "A picture of one or more maps with no frame of its own, from world.canvas, for a frame display, a hand or a screen."
---

A picture of one or more maps with no frame of its own, from `world.canvas`, for a frame display, a hand or a screen.

[`Picture`](/ref/Picture/)

## Functions

| Call                              | Purpose                                                                                                                                           |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`view`](/ref/Canvas/view/)       | The map id of its top-left map, for a `filled_map`. Returns that player's own layer over the canvas, drawn with the same calls; only they see it. |
| [`destroy`](/ref/Canvas/destroy/) | Removes the canvas; clients that saw it keep its last picture, and its id is never reused.                                                        |
