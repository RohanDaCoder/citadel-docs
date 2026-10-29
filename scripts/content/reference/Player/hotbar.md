---
title: "player:hotbar"
url: /docs/citadel/reference/Player/hotbar
---

# player:hotbar

Replaces the nine hotbar slots; a missing index is empty.

```
player:hotbar(slots: { [number]: ItemTable })
```


## Parameters


## Used in
- [`player:hotbar{ [1] = { item = "lapis_block", name = "Tap me" } }`Scoreboard with a button](/docs/citadel/scoreboard-with-a-button)
- [`player:hotbar{ -- replaces the nine hotbar slots; a missing index is empty`Hotbar menus](/docs/citadel/hotbar-menus)
- [`player:hotbar{ [9] = { item = "player_head", skin = player.name, name = "Profile" } }`Items](/docs/citadel/items)
