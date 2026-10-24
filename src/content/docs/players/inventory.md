---
title: "Inventory and items"
description: "ItemSpec forms — a name or a table with count, name, lore, colours, glint, canvas, id, damage, model and skin — the give/take/count/inventory/held calls, pack items, head items, armour via wear, and recipes."
---

:::note[In short]
an item is a name (`"stone"`) or a table (`{ item = "arrow",
count = 16 }`) carrying its meta. `player:give`, `take`, `inventory`,
`count`, `held` and `set_held` work on inventory stacks — given items merge,
hotbar first, and overflow is dropped, not duplicated. A pack can mint its
own items with `id`, give heads a face with `skin`, fill the four armour
slots with `wear`, and add crafting recipes.
:::

## An item is a name or a table

An `ItemSpec` is a string or an `ItemTable`; every call that takes an item
takes either form.

```luau
"potion"                             -- just the item
{
    item = "potion",                 -- required in a table
    count = 2,                       -- 1 by default
    name = "Lime Laser",             -- text; never italic unless it says so
    lore = { "a laser follows you" },  -- lines under the name, grey unless they say; one text is one line
    color = colors.lime,             -- a potion's liquid
    dye = color(0.2, 0.5, 1),        -- leather armour's colour
    glint = true,                    -- the enchanted shine, with no enchantment
    canvas = c,                      -- a filled map of that canvas; then `item` may be left out
}
{ item = "player_head", skin = player.name }   -- a head with a face; see "head items"
```

With `canvas = c`, the item becomes `filled_map` unless you name another. The
table fields are the `ItemMeta`:

| Field    | Meaning                                                                     |
| -------- | --------------------------------------------------------------------------- |
| `count`  | How many in the stack; 1 by default.                                        |
| `name`   | Text; never italic unless it says so.                                       |
| `lore`   | One line or a list of lines, grey unless they say otherwise.                |
| `color`  | A potion's liquid colour; 1.11 and later.                                   |
| `dye`    | Leather armour's colour.                                                    |
| `glint`  | The enchanted shine, with no enchantment.                                   |
| `canvas` | A filled map of that canvas: what the item _is_, so `item` may be left out. |
| `id`     | A pack's own item (below).                                                  |
| `damage` | The wear a tool has taken; 0 is new.                                        |
| `model`  | The item model a 1.21.4+ client draws: `assets/<pack>/items/<model>.json`.  |
| `skin`   | The face a `"player_head"` item shows. On any other item it is an error.    |

## give, take, count, inventory, held

| Call                                                        | Returns             | Purpose                                                   |
| ----------------------------------------------------------- | ------------------- | --------------------------------------------------------- |
| [`player:give(item: ItemSpec)`](/ref/Player/give/)          | —                   | Puts a stack in the inventory.                            |
| [`player:take(item: ItemMatch, count?)`](/ref/Player/take/) | number              | Removes up to `count` (1 unless you say), the hand first. |
| [`player:count(item: ItemMatch)`](/ref/Player/count/)       | number              | How many the player carries, across every slot.           |
| [`player:inventory()`](/ref/Player/inventory/)              | `{ InventorySlot }` | One `{ item, count }` row per filled slot.                |
| [`player:held()`](/ref/Player/held/)                        | `InventorySlot?`    | The stack in hand, or nil.                                |
| [`player:set_held(item?)`](/ref/Player/set_held/)           | —                   | Replaces the stack in hand; nil or false empties it.      |
| [`player:hotbar(slots)`](/ref/Player/hotbar/)               | —                   | Replaces the nine hotbar slots; a missing index is empty. |
| [`player:set_slot(n)`](/ref/Player/set_slot/)               | —                   | Selects hotbar slot 1..9.                                 |

The give/take contract:

- A given stack merges into existing stacks, hotbar first.
- What does not fit is dropped from the give, not duplicated.
- `take` takes up to `count` of what matches, the hand first, and answers how
  many it took.

A stack as a script reads it is an `InventorySlot` — `{ item, count }`, plus
`id` for a pack item and `damage` for a worn tool. An `ItemMatch` (what
`take`, `count`, a recipe's ingredient accept) is a name or a table matching
the fields it names; see [pack items](#pack-items-id) below.

## The player's own window

Clicks in the player's own window work as in the game, all seven click modes
included.

- A pack's own menu over the inventory is `player.ui.menu{}` — see
  [Menus](/ui/menus/).
- A chest's stacks are [`world.container`](/ref/World/container/) — `items()`
  to read them, `take`/`put` to move them.

## Pack items: `id`

`id` makes an item the pack's own. The client draws the base item with its
`name` and `lore`. The server knows it by its `id` everywhere, across
restarts.

Where a call _finds_ an item (`take`, `count`, a recipe, a container):

- A name matches the plain item only.
- A table matches by the fields it names. `{ id = "x" }` is that pack item,
  whatever its base.
- A pack item stacks only with the same pack item. Only your own recipes (see
  [recipes](#recipes)) take it.

`id` is a lower-case word, kept under your pack's name. Your ids read back
bare, another pack's as `"pack:word"`. Either spelling works. `model` is the
item definition that clients from 1.21.4 draw — `model = "copper_ingot"` is
`assets/<pack>/items/copper_ingot.json`; `game.items.define` sets it. Set it
by hand only for a file you shipped in `assets/`.

`damage` is a tool's wear bar. `0` is new. Past its maximum, the tool breaks.
Read it from `held()`; write it with `set_held`.

The base item sets the look and what it does in a hand. A pack pickaxe mines.
A pack block places that block, unless its `id` names a block of yours (see
[Custom blocks](/world/custom-blocks/)).

## Items with their own pictures

`game.items.define` returns an item table for anywhere an item goes:

```luau
local ingot = game.texture(16, 16)       -- a picture drawn in code, or a PNG file in the pack
ingot:rect(2, 6, 12, 5, "#d9822b")
ingot:rect(3, 6, 10, 1, "#f0a860")
local COPPER = game.items.define {
    name = "copper_ingot",                -- its id; the pack's namespace is added
    texture = ingot,                      -- or "textures/copper_ingot.png"
    label = "Copper Ingot",               -- its name; left out, "Copper Ingot" from the id anyway
    lore = { "Smelted from copper ore" },
}
player:give(COPPER)                       -- { ..., count = 4 } for more: COPPER is a plain table
player:take(COPPER, 2)                    -- an item table matches by its id
game.recipes.smelt{ input = ORE, result = COPPER }
```

- `looks` is the vanilla item underneath. Clients below 1.21.4 draw it. It
  sets what the item does in a hand.
  - Default: `paper` (stacks to 64, does nothing).
  - With `stack = 1`, the default is `carrot_on_a_stick`.
  - Name a pickaxe for a tool that mines, a sword for one that hits.
- `texture` is drawn flat in a hand and in the inventory. Vanilla items are 16
  by 16.
- Define items while the pack loads.

A texture's colours are any colour the API takes; `colors.transparent` is
see-through. Where a call takes a texture, a string names a PNG file in the
pack.

## Head items

A `"player_head"` item shows a face when you give it a `skin`. It works
everywhere an item goes: a hotbar slot, a menu, a hand, a display, a chest.

```luau
player:hotbar{ [9] = { item = "player_head", skin = player.name, name = "Profile" } }
player:give{ item = "player_head", skin = player.name }
player:give{ item = "player_head", skin = { value = "ewogICJ0aW1l...", signature = "..." } }
```

- `skin` takes the same forms as a placed head: a player's name, or
  `{ value = , signature = }`.
- The name of a player in the room uses the skin they joined with. This costs
  nothing.
- Any other name is looked up from Mojang once, in the background:
  - Clients from 1.20.5 look the name up themselves and show the face.
  - Older clients show a plain head the first time. Make the item again (for
    example, set the hotbar on the next join) and they show the face.
  - A name with no account shows a plain head and logs one line.
- The face stays with the item: in the player's file, in a chest, on the
  ground.
- `skin` on any other item is an error.
- Clients from 1.7 see the face. Bedrock clients see a plain head.

## Armour: `wear`

```luau
player:wear{ head = "iron_helmet", chest = { item = "leather_chestplate", dye = colors.blue },
             legs = "chainmail_leggings", feet = "golden_boots" }
player:wear{ head = "carved_pumpkin" }   -- replaces all four: the three left out are bare
player:wear{}                            -- all off
npc:wear{ chest = "diamond_chestplate" } -- the same on an npc
```

`wear` fills the armour slots of a player or an npc. Each piece is an item
(see above), so `dye` and `glint` work. The `Worn` table has `head`, `chest`,
`legs` and `feet`, each an `ItemSpec`.

- The inventory, the body and the armour bar show the pieces. Armour does not
  reduce damage yet.
- Nearby clients draw the pieces from 1.8.
- Any item goes on the head. Other slots draw only armour made for them.
- On a pack server, only the pack takes armour off.
- On a survival server, these are the real armour slots. `wear` replaces their
  contents, and the player can take pieces off.

## Recipes

Add recipes at the top of `main.luau`, while the pack loads. A reload replaces
the pack's recipe list.

```luau
game.recipes.shaped{
    pattern = { "CCC", "CMC", "CCC" },    -- 1 to 3 rows of 1 to 3 letters; a space is an empty cell
    keys = { C = { id = "copper_cable" }, M = "iron_block" },
    result = macerator.item,              -- an item, with its count: { ..., count = 4 }
}
game.recipes.shapeless{ items = { "coal", "coal", { id = "iron_dust" } }, result = STEEL }
game.recipes.smelt{ input = { id = "copper_dust" }, result = COPPER }
```

- An ingredient is an item to match (see [pack items](#pack-items-id)): a
  name, or `{ id = ... }`.
- A shaped recipe matches anywhere it fits in the grid, and mirrored.
- The 2x2 inventory grid takes recipes that fit in it. The crafting table
  takes all.
- Vanilla recipes are checked first. A pack adds recipes and never removes
  one.
- A furnace smelts a pack item only through a `smelt` recipe. No pack item
  burns as fuel.

## How clients show the meta

The engine writes the meta in each client's format: NBT tags up to 1.20.4,
data components from 1.20.5. A field a version cannot show is left out. A
potion's colour needs 1.11. No other field has a version limit.

```luau
player:give{ item = "potion", name = "Lime Laser", color = colors.lime, lore = { "30 seconds" } }
npc:hold{ item = "potion", color = colors.lime }
world.display{ kind = "item", item = { item = "potion", color = colors.lime }, at = vec3(0.5, 66, 2.5) }
```

## See also

- [Menus](/ui/menus/) — `player.ui.menu{}` over the inventory, hotbar menus.
- [Game data](/world/game-data/) — `game.item(name)` and the game's own items.
- [Displays](/ui/displays/) — items posed in the world (`context`, `worn`, `held`).
- [Custom blocks](/world/custom-blocks/) — a pack block whose `id` names a block.
- [Kits](/cookbook/cookbook-kits/) — giving sets of items in practice.
