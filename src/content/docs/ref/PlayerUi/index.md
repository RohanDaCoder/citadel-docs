---
title: "PlayerUi type"
description: "player.ui: the calls ui has, for one player alone, plus what only one player's screen holds."
---

`player.ui`: the calls `ui` has, for one player alone, plus what only one player's screen holds.

[`Ui`](/ref/Ui/)

## Functions

| Call                                | Purpose                                                                                                                                                                                                                                                                                                                  |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`menu`](/ref/PlayerUi/menu/)       | A titled grid of up to 54 items over the player's view; each pick is answered by `on_pick(player, n)`. Nothing goes in or out of it: the items are pictures, not stacks. A chest on Java, a form of buttons on Bedrock. `on_close` fires when the player puts it away without picking. A new menu replaces the open one. |
| [`overlay`](/ref/PlayerUi/overlay/) | Puts a canvas in a corner of this player's screen, `size` screen pixels square at GUI scale 1 (96 by default, 16 to 511), `margin` from the edges (4 by default); nil where `player:supports("overlay")` is false.                                                                                                       |
| [`show`](/ref/PlayerUi/show/)       | Puts a layout on this player's screen. A client older than 1.21.4 (`player:supports("layout")`) gets a handle that shows nothing.                                                                                                                                                                                        |
| [`dialog`](/ref/PlayerUi/dialog/)   | A screen of boxes, words and pictures (see "Dialogs"): a `ui.kit.window{}`, or a function that returns one and is drawn again after every click. nil where `player:supports("dialog")` is false.                                                                                                                         |
