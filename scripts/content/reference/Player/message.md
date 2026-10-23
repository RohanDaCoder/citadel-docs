---
title: "player:message"
url: /docs/citadel/reference/Player/message
---

# player:message

What shows on this player's screen: the calls `ui` has, for them alone, plus their own menu and overlay. Sends a chat line to this player alone; `color` is for the words that did not pick one. Chat is not part of the screen, so it is not in `ui`.

```
player:message(text: Text, color: Ink?)
```


## Parameters


## Used in
- [`player:message("Walk around, then type /spawn to return to the gold block.", "aqua")`Guide: Your first pack](/docs/citadel/guides/your-first-pack)
- [`reads their name; `player.ui.title` shows them a title; `player:message``Guide: Your first pack](/docs/citadel/guides/your-first-pack)
- [`player:message(`Walk onto the gold plates! Your best is {best}.`, "gold")`Guide: Coin rush](/docs/citadel/guides/coin-rush)
- [`player:message(`Walk onto the gold plates! Your best is {best}.`, "gold")`Guide: Coin rush](/docs/citadel/guides/coin-rush)
- [`player:message(`Your best time is {string.format("%.1f s", best)}.`, "green")`Guide: Parkour, a room each](/docs/citadel/guides/parkour-a-room-each)
- [`player:message(`Your best time is {string.format("%.1f s", best)}.`, "green")`Guide: Parkour, a room each](/docs/citadel/guides/parkour-a-room-each)
- [`player:message("Walk around, then type /spawn to return to the gold block.", "aqua")`Your first pack](/docs/citadel/your-first-pack)
- [`player:message("You are back at spawn.", "green")`Your first pack](/docs/citadel/your-first-pack)
