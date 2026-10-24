---
title: "entitySpec.on_damage"
description: 'Asked when a player hits it: answer "take" or "ignore"'
---

Part of [`entitySpec`](/ref/EntitySpec/).

```luau
entitySpec.on_damage((e: EntityHandle, amount: number, by: Player ?) -> ("take" | "ignore")?) → ?
```

Asked when a player hits it: answer "take" or "ignore". Nil or a missed deadline is "take". `by` is the player who hit.

## Parameters

| Name | Type                                                                      | Required |
| ---- | ------------------------------------------------------------------------- | -------- |
| `(e` | `EntityHandle , amount: number , by: Player ?) -> ( "take" \| "ignore" )` | no       |

## Returns

- `?`
