---
title: 'blocks.define'
description: 'Load-time only: a world may already be holding blocks of a definition, so one that arrived later would change the rules under the players standing on it'
---

Part of [`blocks`](/ref/Blocks/).

```luau
blocks.define(spec: BlockSpec) → BlockDef
```

Load-time only: a world may already be holding blocks of a definition, so one that arrived later would change the rules under the players standing on it. Define at the top of `main.luau`.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `spec` | [`BlockSpec`](/ref/BlockSpec/) | yes |

## Returns

- [`BlockDef`](/ref/BlockDef/)

## Used in

> "Set `texture` in `game.items.define` and `game.blocks.define` (below). The" — [Packs](/concepts/pack-anatomy/)
> "`game.blocks.define` gives a pack its own block:" — [Custom blocks](/world/custom-blocks/)
> "local crate = game.blocks.define {" — [Custom blocks](/world/custom-blocks/)
> "- Use it for the game's blocks. A block from `game.blocks.define` leaves the" — [Game data](/world/game-data/)
