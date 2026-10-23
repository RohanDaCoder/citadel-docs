---
title: 'ui.title'
description: 'Shows a title and subtitle to everyone in the room; fades and stay are in seconds.'
---

Part of [`ui`](/ref/Ui/).

```luau
ui.title(opts: { title: Text ?, subtitle: Text ?, color: Ink ?, fade_in: number ?, stay: number ?, fade_out: number ?, })
```

Shows a title and subtitle to everyone in the room; fades and stay are in seconds.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `opts` | `{ title: Text ?, subtitle: Text ?, color: Ink ?, fade_in: number ?, stay: number ?, fade_out: number ?, }` | yes |

## Used in

> "player.ui.title{" — [Guide: Your first pack](/getting-started/quick-start/)
> "reads their name; `player.ui.title` shows them a title; `player:message`" — [Guide: Your first pack](/getting-started/quick-start/)
> "ui.title{ title = "GO!", color = "gold", stay = 1 }" — [Guide: Coin rush](/guides/guide-coin-rush/)
> "ui.title{ title = `{winner.name} wins`, subtitle = coins_text(most), color = "gold" }" — [Guide: Coin rush](/guides/guide-coin-rush/)
> "player.ui.title{ title = "Parkour", subtitle = "Type /play", color = "green" }" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
> "p.ui.title{ title = seconds(t), subtitle = "Finished!", color = "green" }" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
