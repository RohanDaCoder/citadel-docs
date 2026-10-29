---
title: "players.on_click"
url: /docs/citadel/reference/Players/on_click
---

# players.on_click

Calls `fn` on a left or right click; `hit` holds the button and the entity, player, block and face it met.

```
players.on_click(fn: (player: Player, hit: Hit) -> ()) → Connection
```


## Parameters


## Returns


## Used in
- [`players.on_click(function(player, hit)`Scoreboard with a button](/docs/citadel/scoreboard-with-a-button)
- [`players.on_click(function(player, hit) end) -> connection`Input](/docs/citadel/input)
- [`- A click while holding a slot fires `players.on_click` with `hit.slot``Hotbar menus](/docs/citadel/hotbar-menus)
- [`hit.slot -- on every players.on_click, 1..9`Hotbar menus](/docs/citadel/hotbar-menus)
- [`- `players.on_click` still gets the click, with the frame's `entity_id` and`Screens](/docs/citadel/screens)
- [`d.id -- entity id, what players.on_click reports in hit.entity_id`Displays](/docs/citadel/displays)
- [``players.on_click`. Clients below 1.19.4 get no hitbox.`Displays](/docs/citadel/displays)
- [`n.id -- entity id, what players.on_click reports in hit.entity_id`NPCs](/docs/citadel/npcs)
