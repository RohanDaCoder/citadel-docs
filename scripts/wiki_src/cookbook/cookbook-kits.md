---
title: Kits
section: cookbook
order: 4
description: Give players starter kits with player:give — inventory merging rules, taking items back, replacing the whole loadout, and hotbar shortcuts for one-click kits.
tags: [kit, give, take, inventory, hotbar, pattern]
---

# Kits

> **In short:** a kit is a loop of `player:give` calls. Understanding the
> three merge rules — hotbar first, stacks merge, overflow drops — makes the
> rest of the pattern obvious. This page covers plain kits, kits that cost
> something, and the hotbar-button form.

## A plain kit

```luau
local KIT = {
    { item = "iron_sword" },
    { item = "cooked_beef", count = 8 },
    { item = "oak_planks", count = 32 },
}

commands.add("kit", function(player)
    for _, stack in KIT do
        player:give(stack)
    end
    player:message("Kit delivered.", "green")
end, { help = "Claim your starter kit" })
```

What `player:give` does with each stack:

- A given stack **merges into existing stacks, hotbar first**.
- What does not fit is **dropped from the give, not duplicated** — count what
  you need before sending a full inventory.
- One item is a bare string (`"stone"`), several are `{ item = "arrow",
count = 16 }`. A pack's own item carries its `id`.

## A kit that costs something

`player:take(item, count)` removes up to `count` of what matches, the hand
first, and **answers how many it took** — that return value is the whole
trick:

```luau
commands.add("kit stone", function(player)
    local took = player:take("cobblestone", 16)
    if took < 16 then
        player:give({ item = "cobblestone", count = took })   -- give the change back
        player:message("You need 16 cobblestone.", "red")
        return
    end
    player:give({ item = "stone_sword" })
    player:give({ item = "stone_pickaxe" })
end, { help = "Trade 16 cobblestone for stone tools" })
```

`player:count(item)` asks without taking — use it to grey out a menu entry or
skip a prompt entirely.

## Replacing the whole loadout

`player:set_held(item)` replaces the stack in hand (`nil` or `false` empties
it), and `player:inventory()` lists one `{ item, count }` row per filled
slot. To clear everything and hand out a fresh kit:

```luau
commands.add("reset", function(player)
    for _, slot in player:inventory() do
        player:take(slot.item, slot.count)
    end
    for _, stack in KIT do
        player:give(stack)
    end
end)
```

## The one-click kit: a hotbar button

The smallest useful kit is a named item in the hotbar that acts when used —
this is the "Scoreboard with a button" form:

```luau
players.on_join(function(player)
    player:hotbar{ [1] = { item = "lapis_block", name = "Kit" } }
end)

players.on_click(function(player, hit)
    if hit.slot ~= 1 or hit.button ~= "right" then return end
    for _, stack in KIT do
        player:give(stack)
    end
end)
```

- `hit.slot` is the hotbar slot number; `hit.button` is `"left"` or
  `"right"`.
- The click event fires for the item in hand wherever the player aims it, so
  the button works anywhere in the world.
- Pair it with the [cooldown](/wiki/cookbook-cooldowns) pattern so it cannot
  be spammed.

## Kits in menus

`player.ui.menu{}` is the many-item version of the hotbar button —
`on_pick` receives the index chosen:

```luau
commands.add("kits", function(player)
    player.ui.menu{
        title = "Choose a kit",
        items = {
            { item = "iron_sword", name = "Warrior", lore = { "sword + beef" } },
            { item = "bow", name = "Archer", lore = { "bow + arrows" } },
        },
        on_pick = function(p, n)
            if n == 1 then p:give("iron_sword"); p:give({ item = "cooked_beef", count = 4 })
            elseif n == 2 then p:give("bow"); p:give({ item = "arrow", count = 16 })
            end
        end,
    }
end)
```

## See also

- [Inventory and items](/wiki/inventory) — every inventory call and the
  ItemSpec forms.
- [Menus](/wiki/menus) — the full menu options.
- [Cooldowns](/wiki/cookbook-cooldowns) — rate-limiting kit claims.
