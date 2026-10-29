---
title: 'recipes.smelt'
description: 'Adds a furnace recipe; a furnace smelts a pack item only by one of these.'
---

Part of [`recipes`](/ref/Recipes/).

```luau
recipes.smelt(spec: { input: ItemMatch, result: ItemSpec })
```

Adds a furnace recipe; a furnace smelts a pack item only by one of these.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `spec` | `{ input: ItemMatch , result: ItemSpec }` | yes |

## Used in

> "game.recipes.smelt{ input = ORE, result = COPPER }" — [Items](/players/inventory/)
> "game.recipes.smelt{ input = { id = "copper_dust" }, result = COPPER }" — [Items](/players/inventory/)
