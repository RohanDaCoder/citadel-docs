---
title: "Bar type"
description: "A boss bar, from ui.bossbar for the room or player.ui.bossbar for one player; title, progress and colour are live."
---

A boss bar, from `ui.bossbar` for the room or `player.ui.bossbar` for one player; title, progress and colour are live.

## Functions

| Call                           | Purpose          |
| ------------------------------ | ---------------- |
| [`destroy`](/ref/Bar/destroy/) | Removes the bar. |

## Fields

| Field                                         | Purpose                                                                                    |
| --------------------------------------------- | ------------------------------------------------------------------------------------------ |
| [`bar.title: Text`](/ref/Bar/title/)          | Reads back the words; takes any text.                                                      |
| [`bar.progress: number`](/ref/Bar/progress/)  | How full the bar is, 0 to 1; live.                                                         |
| [`bar.color: BarColor`](/ref/Bar/color/)      | The bar's colour, from its own closed set; anything else is white. Live.                   |
| [`bar.visible: boolean ?`](/ref/Bar/visible/) | Whether players see the bar; false takes it off their screens, true or nil shows it again. |
