---
title: 'fields global'
description: 'Recipes for numbers over the world, for world.generate.'
---

Recipes for numbers over the world, for `world.generate`.

Part of the [Terrain generation](/world/terrain-generation/) article.

## Functions

| Call | Purpose |
| --- | --- |
| [`noise`](/ref/fields/noise/) | Smooth noise, about -1..1. `solid = true` changes with y too. |
| [`mix`](/ref/fields/mix/) | `a` where `t` is 0, `b` where it is 1. |
| [`hash`](/ref/fields/hash/) | One number 0..1 for each square of `cell` blocks (1). |
| [`cells`](/ref/fields/cells/) | A scattered grid, one point per `size` blocks: the distance to the nearest point, and that point's own number 0..1. |

## Fields

| Field | Purpose |
| --- | --- |
| [`fields.x: Field`](/ref/fields/x/) |  |
| [`fields.y: Field`](/ref/fields/y/) |  |
| [`fields.z: Field`](/ref/fields/z/) |  |
| [`fields.height: Field`](/ref/fields/height/) | The y of the surface of a column, as a block. |
| [`fields.slope: Field`](/ref/fields/slope/) | The step to the steepest of the four columns beside this one. |
| [`fields.water: Field`](/ref/fields/water/) | How deep the water is over the surface; 0 and below on land. |
| [`fields.shore: Field`](/ref/fields/shore/) | 1 on a column at the water's edge with water beside it. |
| [`fields.depth: Field`](/ref/fields/depth/) | Blocks under the surface: `fields.height - fields.y`. |
| [`fields.room: Field`](/ref/fields/room/) | The height of the open space a block is in: 0 in rock, 64 at most (and in the open sky). `density` cannot use it. |
