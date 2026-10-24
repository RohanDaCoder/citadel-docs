---
title: "ModelPart type"
description: "A named group of boxes that turns around its pivot"
---

A named group of boxes that turns around its pivot. Units are 16 to the block, the origin is the model's bottom centre, and a box reaches -24..24.

## Functions

| Call                               | Purpose                                                                                                                                                                                                                                                                              |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`part`](/ref/ModelPart/part/)     | Makes a child part of this one; it turns around `pivot`, the model's origin unless you give one.                                                                                                                                                                                     |
| [`box`](/ref/ModelPart/box/)       | Corners in any order; a box turns on one axis, in steps of 22.5 up to 45, and `pivot` is the box's own centre unless you give one.                                                                                                                                                   |
| [`hitbox`](/ref/ModelPart/hitbox/) | A box a player can hit on a living body that wears the model (clients from 1.19.4). Not drawn; corners in any order, in model units. Square from above (its longer side), so split a long part. Animations do not move it. A model with none is hit on one box of the body's `size`. |
| [`mirror`](/ref/ModelPart/mirror/) | A mirrored copy of every box and hitbox this part has, and a mirrored twin named `<name>_mirrored` of every child. Only "x" in this version.                                                                                                                                         |
