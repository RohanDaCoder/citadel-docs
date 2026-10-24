---
title: 'ItemMeta type'
description: 'The extras an item table may carry: count, name, lore, colours, glint, a canvas map, a pack item id, wear, a 1.21.4+ model and a head''s skin.'
---

The extras an item table may carry: count, name, lore, colours, glint, a canvas map, a pack item id, wear, a 1.21.4+ model and a head's skin.

## Fields

| Field | Purpose |
| --- | --- |
| [`itemMeta.count: number ?`](/ref/ItemMeta/count/) | How many in the stack; 1 by default. |
| [`itemMeta.name: Text ?`](/ref/ItemMeta/name/) | Never italic unless it says so. |
| [`itemMeta.lore: ({ Text } \| Text)?`](/ref/ItemMeta/lore/) | One line or a list of lines, grey unless they say otherwise. |
| [`itemMeta.color: Color ?`](/ref/ItemMeta/color/) | A potion's liquid colour; 1.11 and later. |
| [`itemMeta.dye: Color ?`](/ref/ItemMeta/dye/) | Leather armour's colour. |
| [`itemMeta.glint: boolean ?`](/ref/ItemMeta/glint/) | The enchanted shine, with no enchantment. |
| [`itemMeta.canvas: Canvas ?`](/ref/ItemMeta/canvas/) | A filled map of that canvas: what the item *is*, so `item` may be left out. Everywhere an item is taken — a hand, a hotbar slot, a display. |
| [`itemMeta.id: string ?`](/ref/ItemMeta/id/) | A pack's own item: a brick with `id = "copper_ingot"` is a copper ingot, kept under the pack's name and known by it everywhere it goes. |
| [`itemMeta.damage: number ?`](/ref/ItemMeta/damage/) | The wear a tool has taken; 0 is new. |
| [`itemMeta.model: string ?`](/ref/ItemMeta/model/) | The item model a 1.21.4+ client draws: `assets/<pack>/items/<model>.json`. |
| [`itemMeta.skin: (string \| { value: string, signature: string ? })?`](/ref/ItemMeta/skin/) | The face a "player_head" item shows: a player's name, or the raw `textures` property. On any other item it is an error. |
