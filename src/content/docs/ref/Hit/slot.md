---
title: 'hit.slot'
description: 'The hotbar slot in hand, 1..9.'
---

Part of [`hit`](/ref/Hit/).

```luau
hit.slot: number
```

The hotbar slot in hand, 1..9.

## Used in

> "if hit.slot ~= 1 or hit.button ~= "right" then" — [Scoreboard with a button](/guides/guide-scoreboard-with-a-button/)
> "- A click while holding a slot fires `players.on_click` with `hit.slot`" — [Hotbar menus](/ui/menus/)
> "hit.slot                             -- on every players.on_click, 1..9" — [Hotbar menus](/ui/menus/)
