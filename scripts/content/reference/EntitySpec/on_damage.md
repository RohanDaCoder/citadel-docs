---
title: "entitySpec.on_damage"
url: /docs/citadel/reference/EntitySpec/on_damage
---

# entitySpec.on_damage

Asked when a player hits it: answer "take" or "ignore". Nil or a missed deadline is "take". `by` is the player who hit.

```
entitySpec.on_damage((e: EntityHandle, amount: number, by: Player?) -> ("take" | "ignore")?) → ?
```


## Parameters


## Returns
