---
title: "entities.names"
url: /docs/citadel/reference/Entities/names
---

# entities.names

Every kind by name: the pack's own and the game's, mob or not. `mob = true` gives the mob kinds only, `mob = false` the rest.

```
entities.names(query: { mob: boolean? }?) → { string }
```


## Parameters


## Returns


## Used in
- [`game.entities.names { mob = true } -- {"pig", "sheep", "cow", ...}`Game data](/docs/citadel/game-data)
- [`game.entities.names() -- every kind: the pack's own and the game's, mob or not`Game data](/docs/citadel/game-data)
