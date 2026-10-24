---
title: 'entities.names'
description: 'Every kind by name: the pack''s own and the game''s, mob or not'
---

Part of [`entities`](/ref/Entities/).

```luau
entities.names(query: { mob: boolean ? }?) → { string }
```

Every kind by name: the pack's own and the game's, mob or not. `mob = true` gives the mob kinds only, `mob = false` the rest.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `query` | `{ mob: boolean ? }` | no |

## Returns

- `{ string }`

## Used in

> "game.entities.names { mob = true }   -- {"pig", "sheep", "cow", ...}" — [Game data](/world/game-data/)
> "game.entities.names()                    -- every kind: the pack's own and the game's, mob or not" — [Game data](/world/game-data/)
