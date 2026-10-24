---
title: "Hud type"
description: "A layout on one player's screen, from player.ui.show"
---

A layout on one player's screen, from `player.ui.show`. `hud.<id>` is the item with that id.

## Functions

| Call                           | Purpose                                                                                                                                     |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- |
| [`set`](/ref/Hud/set/)         | A value per id: a number is a fill, a string a label's words, true or false whether it shows. An unknown id is an error that lists the ids. |
| [`destroy`](/ref/Hud/destroy/) | Takes it off the player's screen.                                                                                                           |
