# SOURCE: Items

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
With `canvas = c`, the item becomes `filled_map` unless you name another.
## Head items
A `"player_head"` item shows a face when you give it a `skin`. It works
everywhere an item goes: a hotbar slot, a menu, a hand, a display, a chest.
```luau
player:hotbar{ [9] = { item = "player_head", skin = player.name, name = "Profile" } }
player:give{ item = "player_head", skin = "Notch" }
player:give{ item = "player_head", skin = { value = "ewogICJ0aW1l...", signature = "..." } }
```
- `skin` takes the same forms as a placed head (see “player heads”): a
player’s name, or `{ value = , signature = }`.
- The name of a player in the room uses the skin they joined with. This
costs nothing.
- Any other name is looked up from Mojang once, in the background:
  - Clients from 1.20.5 look the name up themselves and show the face.
  - Older clients show a plain head the first time. Make the item again
(for example, set the hotbar on the next join) and they show the face.
  - A name with no account shows a plain head and logs one line.
- The face stays with the item: in the player’s file, in a chest, on the
ground.
- `skin` on any other item is an error.
- Clients from 1.7 see the face. Bedrock clients see a plain head.
## Items of your own
`id` makes an item the pack’s own. The client draws the base item with its
`name` and `lore`. The server knows it by its `id` everywhere, across
restarts.
The rules:
- Where a call *finds* an item (`take`, `count`, a recipe, a container):
  - A name matches the plain item only.
  - A table matches by the fields it names. `{ id = "x" }` is that pack
item, whatever its base.
- A pack item stacks only with the same pack item. Only your own recipes
(see “recipes”) take it.
- `id` is a lower-case word, kept under your pack’s name. Your ids read
back bare, another pack’s as `"pack:word"`. Either spelling works.
- `model` is the item definition that clients from 1.21.4 draw.
`model = "copper_ingot"` is `assets/<pack>/items/copper_ingot.json`.
`game.items.define` sets it. Set it by hand only for a file you shipped in
`assets/`.
- `damage` is a tool’s wear bar. `0` is new. Past its maximum, the tool
breaks. Read it from `held()`; write it with `set_held`.
- The base item sets the look and what it does in a hand. A pack pickaxe
mines. A pack block places that block, unless its `id` names a block of
yours (see “Custom blocks”).
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
- `texture` is drawn flat in a hand and in the inventory. Vanilla items are
16 by 16.
- Define items while the pack loads.
## Drawing a texture
A colour is any colour the API takes. `colors.transparent` is see-through.
Where a call takes a texture, a string names a PNG file in the pack.
## Recipes
Add recipes at the top of `main.luau`, while the pack loads. A reload
replaces the pack’s recipe list.
```luau
game.recipes.shaped{
    pattern = { "CCC", "CMC", "CCC" },    -- 1 to 3 rows of 1 to 3 letters; a space is an empty cell
    keys = { C = { id = "copper_cable" }, M = "iron_block" },
    result = macerator.item,              -- an item, with its count: { ..., count = 4 }
}
game.recipes.shapeless{ items = { "coal", "coal", { id = "iron_dust" } }, result = STEEL }
game.recipes.smelt{ input = { id = "copper_dust" }, result = COPPER }
```
- An ingredient is an item to match (see “items of your own”): a name, or
`{ id = ... }`.
- A shaped recipe matches anywhere it fits in the grid, and mirrored.
- The 2x2 inventory grid takes recipes that fit in it. The crafting table
takes all.
- Vanilla recipes are checked first. A pack adds recipes and never removes
one.
- A furnace smelts a pack item only through a `smelt` recipe. No pack item
burns as fuel.
```luau
player:give{ item = "potion", name = "Lime Laser", color = colors.lime, lore = { "30 seconds" } }
npc:hold{ item = "potion", color = colors.lime }
world.display{ kind = "item", item = { item = "potion", color = colors.lime }, at = vec3(0.5, 66, 2.5) }
```
The engine writes the meta in each client’s format: NBT tags up to 1.20.4,
data components from 1.20.5. A field a version cannot show is left out. A
potion’s colour needs 1.11. No other field has a version limit.
