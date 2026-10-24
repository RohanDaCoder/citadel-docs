---
title: "ui global · type Ui"
description: "Titles, chat, the action bar, boss bars, the sidebar and the tab list: for everyone in a room (the ui global, or room.ui), or for one player (player.ui, the same calls)"
---

Titles, chat, the action bar, boss bars, the sidebar and the tab list: for everyone in a room (the `ui` global, or `room.ui`), or for one player (`player.ui`, the same calls). "Everyone" below is one player on `player.ui`.

Part of the [UI basics](/ui/ui-basics/) article.

## Functions

| Call                              | Purpose                                                                                                                                                                                           |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`title`](/ref/Ui/title/)         | Shows a title and subtitle to everyone in the room; fades and stay are in seconds.                                                                                                                |
| [`actionbar`](/ref/Ui/actionbar/) | Shows a line above the hotbar to everyone in the room.                                                                                                                                            |
| [`bossbar`](/ref/Ui/bossbar/)     | Shows a boss bar to everyone in the room and returns its handle; progress 0..1. 1.8 reads the title on its action bar.                                                                            |
| [`sidebar`](/ref/Ui/sidebar/)     | Sets the sidebar for everyone in the room; lines run top to bottom and only changed lines are sent. nil or false removes the sidebar.                                                             |
| [`tab`](/ref/Ui/tab/)             | Sets the player list's header and footer for everyone in the room.                                                                                                                                |
| [`box`](/ref/Ui/box/)             | The pieces of a layout (see "Layouts"). Sizes are pixels of the game's own HUD; a box is 1 to 256 a side. An item with an `id` is live.                                                           |
| [`image`](/ref/Ui/image/)         |                                                                                                                                                                                                   |
| [`label`](/ref/Ui/label/)         | Words in the client's own letters, space to `~`. Give a label whose words change a `width`.                                                                                                       |
| [`row`](/ref/Ui/row/)             | The children are the list part: `ui.row{ gap = 4, a, b }`.                                                                                                                                        |
| [`column`](/ref/Ui/column/)       |                                                                                                                                                                                                   |
| [`stack`](/ref/Ui/stack/)         |                                                                                                                                                                                                   |
| [`define`](/ref/Ui/define/)       | A layout of one child, centred over the hotbar with its bottom edge `margin` pixels above the screen's (40, or 25 when `hide_hud` takes the hearts and the food away). While the pack loads only. |

## Fields

| Field                                       | Purpose                                                                                                                                                                              |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`ui.kit: { [string]: any }`](/ref/Ui/kit/) | What a dialog is made of (see "Dialogs"): row, column, stack, space, text, image, and window, button, tabs, close, badge, dot, progress, divider, card, grid, theme, mix and SCREEN. |
