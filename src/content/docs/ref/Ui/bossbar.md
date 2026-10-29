---
title: 'ui.bossbar'
description: 'Shows a boss bar to everyone in the room and returns its handle; progress 0..1'
---

Part of [`ui`](/ref/Ui/).

```luau
ui.bossbar(opts: { title: Text ?, color: BarColor ?, progress: number ? }?) → Bar
```

Shows a boss bar to everyone in the room and returns its handle; progress 0..1. 1.8 reads the title on its action bar.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `opts` | `{ title: Text ?, color: BarColor ?, progress: number ? }` | no |

## Returns

- [`Bar`](/ref/Bar/)

## Used in

> "local bar = ui.bossbar{ title = "Coin rush", color = "yellow", progress = 1 }" — [Guide: Coin rush](/guides/guide-coin-rush/)
> "local bar = ui.bossbar{ title = "Coin rush", color = "yellow", progress = 1 }" — [Guide: Coin rush](/guides/guide-coin-rush/)
> "\| `bossbar` \| `ui.bossbar`, `player.ui.bossbar` \| 1.9 \|" — [Client versions](/appendix/client-versions/)
> "local bar = ui.bossbar{ title = "Race starts in 30 s", color = "purple", progress = 1 }" — [HUD](/ui/ui-basics/)
> "local mine = player.ui.bossbar{ title = "Your horse: Lightning" }   -- one player's bar, the same handle" — [HUD](/ui/ui-basics/)
