---
title: 'player:kill'
description: '0..20, or nil where the game version has no food bar'
---

Part of [`Player`](/ref/Player/).

```luau
player:kill() → boolean
```

0..20, or nil where the game version has no food bar. The food saturation, or nil where the game version has no food bar. True while the player is on the death screen. Kills the player; returns false on a version with no damage rules.

## Returns

- `boolean`

## Used in

> "player:kill()          -- true if it happened; false on a version with no damage rules" — [Players](/players/player-lifecycle/)
