---
title: "Recipes type"
description: "game.recipes: what a crafting grid and a furnace make of a pack's items"
---

`game.recipes`: what a crafting grid and a furnace make of a pack's items. Load-time only, like a block definition. The game's own recipes are asked first, so a pack adds and never takes away.

## Functions

| Call                                   | Purpose                                                                   |
| -------------------------------------- | ------------------------------------------------------------------------- |
| [`shaped`](/ref/Recipes/shaped/)       | 1 to 3 rows of 1 to 3 letters; a space is an empty cell.                  |
| [`shapeless`](/ref/Recipes/shapeless/) | Adds a crafting recipe whose ingredients may go anywhere in the grid.     |
| [`smelt`](/ref/Recipes/smelt/)         | Adds a furnace recipe; a furnace smelts a pack item only by one of these. |
