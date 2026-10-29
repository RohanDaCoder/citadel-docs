---
title: 'game.terrain'
description: 'What this world''s overworld is made of: snow and steps, as citadel.yml writes them; read-only, nil when there is no list.'
---

Part of [`game`](/ref/Game/).

```luau
game.terrain: { snow: boolean ?, steps: { TerrainStep }? }?
```

What this world's overworld is made of: `snow` and `steps`, as citadel.yml writes them; read-only, nil when there is no list.

## Used in

> "`game.terrain` prints the original list. Start an edit from it." — [Server settings](/systems/server-settings/)
> "`game.terrain` describes this world's overworld: `snow`, and `steps` in the" — [Game data](/world/game-data/)
> "for i, step in ipairs(game.terrain.steps) do" — [Game data](/world/game-data/)
