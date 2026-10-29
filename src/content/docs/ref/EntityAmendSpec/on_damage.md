---
title: 'entityAmendSpec.on_damage'
description: 'Asked when it takes damage; return "ignore" to cancel it'
---

Part of [`entityAmendSpec`](/ref/EntityAmendSpec/).

```luau
entityAmendSpec.on_damage((e: EntityHandle, amount: number) -> ("take" | "ignore")?) → ?
```

Asked when it takes damage; return "ignore" to cancel it. Silence or a missed deadline is "take".

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `(e` | `EntityHandle , amount: number ) -> ( "take" \| "ignore" )` | no |

## Returns

- `?`
