---
title: 'player.visible'
description: 'false: no other player is sent this body'
---

Part of [`player`](/ref/Player/).

```luau
player.visible: boolean ?
```

false: no other player is sent this body. The tab line stays. true or nil shows the body again.

## Used in

> "- `player.visible = nil` shows the player again, because a player is" — [API basics](/concepts/conventions/)
> "player.visible = false    -- nobody else sees this player; true or nil shows them again; see "who sees whom"" — [Players](/players/player-lifecycle/)
> "player.visible = false        -- from everyone; true or nil brings it back" — [Players](/players/player-lifecycle/)
