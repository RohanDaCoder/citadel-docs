---
title: 'recipes.shapeless'
description: 'Adds a crafting recipe whose ingredients may go anywhere in the grid.'
---

Part of [`recipes`](/ref/Recipes/).

```luau
recipes.shapeless(spec: { items: { ItemMatch }, result: ItemSpec })
```

Adds a crafting recipe whose ingredients may go anywhere in the grid.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `spec` | `{ items: { ItemMatch }, result: ItemSpec }` | yes |

## Used in

> "game.recipes.shapeless{ items = { "coal", "coal", { id = "iron_dust" } }, result = STEEL }" — [Items](/players/inventory/)
