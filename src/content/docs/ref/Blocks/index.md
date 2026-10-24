---
title: "Blocks type"
description: "game.blocks: defines a pack's own blocks and amends the game's own, at load time."
---

`game.blocks`: defines a pack's own blocks and amends the game's own, at load time.

## Functions

| Call                            | Purpose                                                                                                                                                                                     |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`define`](/ref/Blocks/define/) | Load-time only: a world may already be holding blocks of a definition, so one that arrived later would change the rules under the players standing on it. Define at the top of `main.luau`. |
| [`amend`](/ref/Blocks/amend/)   | Only the game's own blocks, never another pack's.                                                                                                                                           |
