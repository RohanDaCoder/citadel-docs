---
title: "player:hotbar"
description: "Replaces the nine hotbar slots; a missing index is empty."
---

Part of [`Player`](/ref/Player/).

```luau
player:hotbar(slots: { [number]: ItemTable })
```

Replaces the nine hotbar slots; a missing index is empty.

## Parameters

| Name    | Type                        | Required |
| ------- | --------------------------- | -------- |
| `slots` | `{ [ number ]: ItemTable }` | yes      |

## Used in

> "player:hotbar{ [1] = { item = "lapis_block", name = "Tap me" } }" — [Scoreboard with a button](/guides/guide-scoreboard-with-a-button/)
> "player:hotbar{ -- replaces the nine hotbar slots; a missing index is empty" — [Hotbar menus](/ui/menus/)
> "player:hotbar{ [9] = { item = "player_head", skin = player.name, name = "Profile" } }" — [Items](/players/inventory/)
