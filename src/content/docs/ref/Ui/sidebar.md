---
title: 'ui.sidebar'
description: 'Sets the sidebar for everyone in the room; lines run top to bottom and only changed lines are sent'
---

Part of [`ui`](/ref/Ui/).

```luau
ui.sidebar(opts: ({ title: Text ?, lines: { Text }? } | false)?)
```

Sets the sidebar for everyone in the room; lines run top to bottom and only changed lines are sent. nil or false removes the sidebar.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `opts` | `({ title: Text ?, lines: { Text }? } \| false )` | no |

## Used in

> "ui.sidebar{ title = "COIN RUSH", lines = lines }" — [Guide: Coin rush](/guides/guide-coin-rush/)
> "ui.sidebar{ title = "COIN RUSH", lines = lines }" — [Guide: Coin rush](/guides/guide-coin-rush/)
> "ui.sidebar{ title = "INDIGO", lines = { "Chips  1200", "Bet  50", "", "Roulette" } }   -- everyone in the room" — [HUD](/ui/ui-basics/)
> "player.ui.sidebar{ title = "INDIGO", lines = { ... } }   -- one player; lines run top to bottom" — [HUD](/ui/ui-basics/)
> "player.ui.sidebar{ title = { "KART", color = "gold", bold = true }, lines = {" — [Text formatting](/ui/ui-basics/)
> "p.ui.sidebar { title = { "KART", effect = rainbow, bold = true } }" — [Text formatting](/ui/ui-basics/)
