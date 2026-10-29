---
title: 'Hud type'
description: 'A layout on one player''s screen, from player.ui.show'
---

A layout on one player's screen, from `player.ui.show`. `hud.<id>` is the item with that id.

## Functions

| Call | Purpose |
| --- | --- |
| [`set`](/ref/Hud/set/) | A value per id: a number is a fill, a string a label's words, true or false whether it shows. An unknown id is an error that lists the ids. |
| [`destroy`](/ref/Hud/destroy/) | Takes it off the player's screen. |
| [`on_hover`](/ref/Hud/on_hover/) |  |
| [`on_click`](/ref/Hud/on_click/) |  |

## Fields

| Field | Purpose |
| --- | --- |
| [`hud.hover: string ?`](/ref/Hud/hover/) | With `cursor = true`: the id under the pointer, and what fires when it changes and on a click. |
| [`hud.cursor: { x: number, y: number }?`](/ref/Hud/cursor/) | Where the pointer is, in the layout's pixels from its top left. |
