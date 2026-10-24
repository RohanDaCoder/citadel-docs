---
title: "player:message"
description: "What shows on this player's screen: the calls ui has, for them alone, plus their own menu and overlay"
---

Part of [`Player`](/ref/Player/).

```luau
player:message(text: Text, color: Ink ?)
```

What shows on this player's screen: the calls `ui` has, for them alone, plus their own menu and overlay. Sends a chat line to this player alone; `color` is for the words that did not pick one. Chat is not part of the screen, so it is not in `ui`.

## Parameters

| Name    | Type                 | Required |
| ------- | -------------------- | -------- |
| `text`  | [`Text`](/ref/Text/) | yes      |
| `color` | [`Ink`](/ref/Ink/)   | no       |

## Used in

> "player:message("Walk around, then type /spawn to return to the gold block.", "aqua")" — [Guide: Your first pack](/getting-started/quick-start/)
> "reads their name; `player.ui.title` shows them a title; `player:message`" — [Guide: Your first pack](/getting-started/quick-start/)
> "player:message(`Walk onto the gold plates! Your best is {best}.`, "gold")" — [Guide: Coin rush](/guides/guide-coin-rush/)
> "player:message(`Walk onto the gold plates! Your best is {best}.`, "gold")" — [Guide: Coin rush](/guides/guide-coin-rush/)
> "player:message(`Your best time is {string.format("%.1f s", best)}.`, "green")" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
> "player:message(`Your best time is {string.format("%.1f s", best)}.`, "green")" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
