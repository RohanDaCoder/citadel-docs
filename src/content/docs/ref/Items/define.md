---
title: 'items.define'
description: 'Load-time only'
---

Part of [`items`](/ref/Items/).

```luau
items.define(spec: { name: string, texture: TextureRef ?, label: Text ?, lore: ({ Text } | Text)?, looks: string ?, stack: number ?, glint: boolean ?, }) → ItemTable
```

Load-time only. Hands back the item table: give it, match it, craft it.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `spec` | `{ name: string , texture: TextureRef ?, label: Text ?, lore: ({ Text } \| Text )?, looks: string ?, stack: number ?, glint: boolean ?, }` | yes |

## Returns

- [`ItemTable`](/ref/ItemTable/)

## Used in

> "Set `texture` in `game.items.define` and `game.blocks.define` (below). The" — [Packs](/concepts/pack-anatomy/)
> "`game.items.define` sets it. Set it by hand only for a file you shipped in" — [Items](/players/inventory/)
> "`game.items.define` returns an item table for anywhere an item goes:" — [Items](/players/inventory/)
