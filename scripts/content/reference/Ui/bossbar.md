---
title: "ui.bossbar"
url: /docs/citadel/reference/Ui/bossbar
---

# ui.bossbar

Shows a boss bar to everyone in the room and returns its handle; progress 0..1. 1.8 reads the title on its action bar.

```
ui.bossbar(opts: { title: Text?, color: BarColor?, progress: number? }?) → Bar
```


## Parameters


## Returns


## Used in
- [`local bar = ui.bossbar{ title = "Coin rush", color = "yellow", progress = 1 }`Guide: Coin rush](/docs/citadel/guides/coin-rush)
- [`local bar = ui.bossbar{ title = "Coin rush", color = "yellow", progress = 1 }`Guide: Coin rush](/docs/citadel/guides/coin-rush)
- [`| `bossbar` | `ui.bossbar`, `player.ui.bossbar` | 1.9 |`Client versions](/docs/citadel/client-versions)
- [`local bar = ui.bossbar{ title = "Race starts in 30 s", color = "purple", progress = 1 }`HUD](/docs/citadel/hud)
- [`local mine = player.ui.bossbar{ title = "Your horse: Lightning" } -- one player's bar, the same handle`HUD](/docs/citadel/hud)
