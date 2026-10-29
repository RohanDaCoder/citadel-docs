---
title: "game.terrain"
url: /docs/citadel/reference/Game/terrain
---

# game.terrain

What this world's overworld is made of: `snow` and `steps`, as citadel.yml writes them; read-only, nil when there is no list.

```
game.terrain: { snow: boolean?, steps: { TerrainStep }? }?
```


## Used in
- [``game.terrain` prints the original list. Start an edit from it.`Server settings](/docs/citadel/server-settings)
- [``game.terrain` describes this world's overworld: `snow`, and `steps` in the`Game data](/docs/citadel/game-data)
- [`for i, step in ipairs(game.terrain.steps) do`Game data](/docs/citadel/game-data)
