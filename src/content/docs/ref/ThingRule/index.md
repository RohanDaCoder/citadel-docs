---
title: 'ThingRule type'
description: 'A thing that stands on a grid cell: one of shapes, its (0, 0, 0) on the block above the ground'
---

A thing that stands on a grid cell: one of `shapes`, its `(0, 0, 0)` on the block above the ground. `afloat` stands it on the water where the ground is under water; without it, nothing stands there. `place = "floor"` puts its `(0, 0, 0)` on the air block over a cave floor, `"ceiling"` on the air block under a ceiling (build it down from there).

`{ shapes: { Schematic }, chance: (Field` | `number)?, biome: string?, when: (Field` | `number)?, afloat: boolean?, place: ("top"` | `"floor"` | `"ceiling")?, y: { number }? }`
