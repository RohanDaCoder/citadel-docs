---
title: "ui.actionbar"
description: "Shows a line above the hotbar to everyone in the room."
---

Part of [`ui`](/ref/Ui/).

```luau
ui.actionbar(text: Text, color: Ink ?)
```

Shows a line above the hotbar to everyone in the room.

## Parameters

| Name    | Type                 | Required |
| ------- | -------------------- | -------- |
| `text`  | [`Text`](/ref/Text/) | yes      |
| `color` | [`Ink`](/ref/Ink/)   | no       |

## Used in

> "player.ui.actionbar(seconds(time.now() - started), "yellow")" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
> "player.ui.actionbar(seconds(time.now() - started), "yellow")" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
> "ui.actionbar(text, color) -- the line above the hotbar, to everyone" — [Titles and bars](/ui/ui-basics/)
> "player.ui.actionbar("Bet 50 · Chips 1200", "light_purple") -- the line above the hotbar" — [HUD](/ui/ui-basics/)
> "`player.ui.actionbar` instead. A client that turns the pack down stops" — [Layouts](/ui/screens/)
> "- A layout uses the action bar. While one shows, `player.ui.actionbar` text" — [Layouts](/ui/screens/)
