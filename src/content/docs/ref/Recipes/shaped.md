---
title: "recipes.shaped"
description: "1 to 3 rows of 1 to 3 letters; a space is an empty cell."
---

Part of [`recipes`](/ref/Recipes/).

```luau
recipes.shaped(spec: { pattern: { string }, keys: { [string]: ItemMatch }, result: ItemSpec })
```

1 to 3 rows of 1 to 3 letters; a space is an empty cell.

## Parameters

| Name   | Type                                                                         | Required |
| ------ | ---------------------------------------------------------------------------- | -------- |
| `spec` | `{ pattern: { string }, keys: { [ string ]: ItemMatch }, result: ItemSpec }` | yes      |

## Used in

> "game.recipes.shaped{ pattern = { "FFF", "F F", "FFF" }, keys = { F = "flint" }, result = macerator.item }" — [Custom blocks](/world/custom-blocks/)
> "game.recipes.shaped{" — [Items](/players/inventory/)
