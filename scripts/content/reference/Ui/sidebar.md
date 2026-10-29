---
title: "ui.sidebar"
url: /docs/citadel/reference/Ui/sidebar
---

# ui.sidebar

Sets the sidebar for everyone in the room; lines run top to bottom and only changed lines are sent. nil or false removes the sidebar.

```
ui.sidebar(opts: ({ title: Text?, lines: { Text }? } | false)?)
```


## Parameters


## Used in
- [`ui.sidebar{ title = "COIN RUSH", lines = lines }`Guide: Coin rush](/docs/citadel/guides/coin-rush)
- [`ui.sidebar{ title = "COIN RUSH", lines = lines }`Guide: Coin rush](/docs/citadel/guides/coin-rush)
- [`ui.sidebar{ title = "INDIGO", lines = { "Chips 1200", "Bet 50", "", "Roulette" } } -- everyone in the room`HUD](/docs/citadel/hud)
- [`player.ui.sidebar{ title = "INDIGO", lines = { ... } } -- one player; lines run top to bottom`HUD](/docs/citadel/hud)
- [`player.ui.sidebar{ title = { "KART", color = "gold", bold = true }, lines = {`Text formatting](/docs/citadel/text-formatting)
- [`p.ui.sidebar { title = { "KART", effect = rainbow, bold = true } }`Text formatting](/docs/citadel/text-formatting)
