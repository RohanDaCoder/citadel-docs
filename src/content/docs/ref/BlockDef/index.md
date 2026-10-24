---
title: 'BlockDef type'
description: 'The handle define hands back'
---

The handle `define` hands back. Equality is identity — two handles are the same block when they name the same block.

## Fields

| Field | Purpose |
| --- | --- |
| [`blockDef.name: string`](/ref/BlockDef/name/) | Canonical, with the pack's namespace already on it: "rave:crate". |
| [`blockDef.states: number`](/ref/BlockDef/states/) | How many states it has; `block.state` counts 1 to this. |
| [`blockDef.item: ItemTable ?`](/ref/BlockDef/item/) | The block as an item, when the definition gave it one: `player:give(def.item)`. |
