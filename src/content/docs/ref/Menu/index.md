---
title: "Menu type"
description: "An open menu, from player.ui.menu."
---

An open menu, from `player.ui.menu`.

## Functions

| Call                            | Purpose                                                                                                                                                                                               |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`destroy`](/ref/Menu/destroy/) | Takes it down and forgets its callbacks. A Bedrock form cannot be taken back: it stays until the player answers, and the answer then lands nowhere.                                                   |
| [`update`](/ref/Menu/update/)   | New pictures in place, the menu left open: a bar that fills, a count that changes. `on_pick` still answers by position. `false` once the player has put it away; a Bedrock form keeps what it showed. |
