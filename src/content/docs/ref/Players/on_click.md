---
title: "players.on_click"
description: "Calls fn on a left or right click; hit holds the button and the entity, player, block and face it met."
---

Part of [`players`](/ref/Players/).

```luau
players.on_click(fn: (player: Player, hit: Hit) -> ()) → Connection
```

Calls `fn` on a left or right click; `hit` holds the button and the entity, player, block and face it met.

## Parameters

| Name | Type                                 | Required |
| ---- | ------------------------------------ | -------- |
| `fn` | `(player: Player , hit: Hit ) -> ()` | yes      |

## Returns

- [`Connection`](/ref/Connection/)

## Used in

> "players.on_click(function(player, hit)" — [Scoreboard with a button](/guides/guide-scoreboard-with-a-button/)
> "players.on_click(function(player, hit) end) -> connection" — [Input](/players/movement/)
> "- A click while holding a slot fires `players.on_click` with `hit.slot`" — [Hotbar menus](/ui/menus/)
> "hit.slot -- on every players.on_click, 1..9" — [Hotbar menus](/ui/menus/)
> "- `players.on_click` still gets the click, with the frame's `entity_id` and" — [Screens](/ui/screens/)
> "d.id -- entity id, what players.on_click reports in hit.entity_id" — [Displays](/ui/displays/)
