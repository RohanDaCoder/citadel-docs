---
title: "player.max_health"
description: "Their health now, 0 to max_health; nil where the game version has no damage rules"
---

Part of [`player`](/ref/Player/).

```luau
player.max_health: number ?
```

Their health now, 0 to `max_health`; nil where the game version has no damage rules. Writable: set outright, no flash; 0 is a death; a number above `max_health` stops there. The most health they can have: 20 unless a pack set it; nil where the game version has no damage rules. Writable, 1 to 1024; nil gives the game's own back. A lower maximum takes `health` down to it. It lasts for the session. Every Java client draws its hearts; Bedrock draws none.

## Used in

> "player.health -- their health now, 0 to player.max_health; nil where the version has no damage rules" — [Players](/players/player-lifecycle/)
> "player.max_health -- the most health they can have: 20 unless a pack set it; nil for the same reason" — [Players](/players/player-lifecycle/)
> "player.health = 20 -- set outright, no flash; 0 is a death; above player.max_health it stops there" — [Body and movement](/players/movement/)
