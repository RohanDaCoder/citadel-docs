---
title: "player.speed"
description: "The body: what a pack sets on a player"
---

Part of [`player`](/ref/Player/).

```luau
player.speed: number
```

The body: what a pack sets on a player. See docs/luau-api.md, "Body and movement". Walk speed as a multiple of normal; 0 pins them.

## Used in

> "Numeric settings such as `player.speed`, `player.scale` and `player.reach`" — [API basics](/concepts/conventions/)
> "player.speed = 2 -- walk speed as a multiple of normal; 0 pins them, 1 is normal" — [Body and movement](/players/movement/)
> "`player.speed = 0` for a cutscene. Do not use `gamemode = 3`." — [Cameras](/players/movement/)
> "}, { easing = "in_out", on_done = function() player.camera = nil player.speed = 1 end })" — [Cameras](/players/movement/)
