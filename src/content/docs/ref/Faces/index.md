---
title: "Faces type"
description: "A block's faces: one picture, or all, side, top, bottom, front, back, or a face by name."
---

A block's faces: one picture, or `all`, `side`, `top`, `bottom`, `front`, `back`, or a face by name.

[`TextureRef`](/ref/TextureRef/) | ``

## Fields

| Field                                                                                                                                              | Purpose                                                                                                             |
| -------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| [`faces.all: TextureRef ?, side: TextureRef ?, top: TextureRef ?, bottom: TextureRef ?`](/ref/Faces/all/)                                          | `all` is one picture for all six faces, `side` for the four sides (`all` if left out), `top` and `bottom` the ends. |
| [`faces.front: TextureRef ?, back: TextureRef ?`](/ref/Faces/front/)                                                                               | `front` is the side a facing block faces and `back` the other; a face left out is `side`.                           |
| [`faces.down: TextureRef ?, up: TextureRef ?, north: TextureRef ?, south: TextureRef ?, west: TextureRef ?, east: TextureRef ?`](/ref/Faces/down/) | One face by its name; a face left out is `side`.                                                                    |
