---
title: "blocks.define"
url: /docs/citadel/reference/Blocks/define
---

# blocks.define

Load-time only: a world may already be holding blocks of a definition, so one that arrived later would change the rules under the players standing on it. Define at the top of `main.luau`.

```
blocks.define(spec: BlockSpec) → BlockDef
```


## Parameters


## Returns


## Used in
- [`Set `texture` in `game.items.define` and `game.blocks.define` (below). The`Packs](/docs/citadel/packs)
- [``game.blocks.define` gives a pack its own block:`Custom blocks](/docs/citadel/custom-blocks)
- [`local crate = game.blocks.define {`Custom blocks](/docs/citadel/custom-blocks)
- [`- Use it for the game's blocks. A block from `game.blocks.define` leaves the`Game data](/docs/citadel/game-data)
