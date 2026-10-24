---
title: 'entityKind.interact'
description: 'Whether a player''s right click on it has the game''s effect (milk, a saddle)'
---

Part of [`entityKind`](/ref/EntityKind/).

```luau
entityKind.interact: boolean ?
```

Whether a player's right click on it has the game's effect (milk, a saddle). `nil`: on for a kind with `spawn = true`, else the room's `survival`. `true` is an error on 1.8.9, which has no right click on a mob.
