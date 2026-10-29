---
title: Menus
section: ui
order: 4
description: player.ui.menu — a titled grid of up to 54 items every client draws, chest on Java and form on Bedrock — and the hotbar as a per-player menu of nine items with live canvas maps.
tags: [ui, menus, hotbar, items, on-pick, bedrock]
---

# Menus

> **In short:** a menu is a titled grid of up to 54 items over the player's
> view. It is not an inventory: the player cannot take or put items; a click
> only picks one. Every client draws one — a chest on Java, a form of buttons
> on Bedrock — so no version check is needed. The hotbar is the other menu:
> nine items set per player, with slot and click events.

## `player.ui.menu`

```luau
commands.add("kit", function(player)
    local m = player.ui.menu{
        title = "Trains",
        items = {
            { item = "coal", name = "Steam locomotive", lore = { "right click a rail holding it" } },
            { item = "redstone", name = "High-speed electric" },
            "iron_ingot",                 -- a bare name works, as everywhere
        },
        on_pick = function(p, n)          -- n is the item picked, 1 up
            p:give(({ "coal", "redstone", "iron_ingot" })[n])
        end,
        on_close = function(p) end,       -- put away without picking
    }
    -- m:destroy() takes it down again; m:update(items) redraws it in place
end)
```

| Option     | What it is                                                                    |
| ---------- | ----------------------------------------------------------------------------- |
| `title`    | The menu's title (text — see [UI basics](/wiki/ui-basics#text-runs))          |
| `items`    | Up to 54 item specs                                                           |
| `on_pick`  | `function(player, n)` — `n` is the item picked, 1 up                          |
| `on_close` | `function(player)` — fired when the player puts the menu away without picking |

## Items

An item is an item (see [Inventory](/wiki/inventory)) with `name`, `lore`,
`color`, `dye`, `glint`, `skin` and `count`. The count shows on the stack, for
a price or a quantity. A bare item name works, as everywhere.

## Every client draws a menu

Java (1.7 to 26.3) shows a chest. Bedrock shows a form with one button per
item, labelled with `name` or the item's name. No `player:supports` check is
needed.

## Picks and closes

- `on_pick` may `task.wait`.
  - On Java the menu stays open. Destroy it in `on_pick` if one pick is enough.
  - A Bedrock form closes on the press. Open it again for another pick.
- [`menu:destroy()`](/ref/Menu/destroy) and a Bedrock pick do not fire `on_close`.
- A new menu replaces the old one.
- Only the pack that opened a menu gets its picks. The menu ends when the
  script ends, the player leaves, or the pack calls `destroy`.

> **Gotcha:** a Bedrock form cannot be taken back: it stays until the player
> answers, and the answer then lands nowhere.

## Updating in place

[`menu:update(items)`](/ref/Menu/update) puts new pictures in place, the menu
left open: a bar that fills, a count that changes. `on_pick` still answers by
position.

- `menu:update` returns `false` once the player has put the menu away; a
  Bedrock form keeps what it showed.
- Under a Java menu, the player's inventory shows. Clicks in it change nothing.

## Hotbar menus

The hotbar is a menu of nine items, set per player.

```luau
player:hotbar{                       -- replaces the nine hotbar slots; a missing index is empty
    [1] = { item = "lapis_block", name = "HIT", count = 1 },
    [7] = { item = "gold_nugget", name = "Bet: 50" },
    [8] = { canvas = minimap, name = "Map" },   -- a filled map of a canvas: a live picture in the hand
}
player.slot                          -- the slot in hand, 1..9, live
hit.slot                             -- on every players.on_click, 1..9
```

The events:

- Selecting a slot fires `players.on_slot`.
- A click while holding a slot fires `players.on_click` with `hit.slot` set.
  Any target and either button counts.
- Right clicks never merge into a hold. The halves of one click (block use,
  item use, both hands) are one event.
- In pack mode the rest of the inventory is locked.

A slot is an item, with the same meta. An item name that the game version
lacks is an error.

> **Tip:** with `canvas = c`, the map shows the picture on every client from
> 1.8, and it updates as the script draws — a live minimap in the hand (see
> [Canvases and pictures](/wiki/canvases)).

## See also

- [Dialogs](/wiki/dialogs) — full-screen dialogs for 1.21.6+ clients, with a menu as the fallback.
- [Inventory](/wiki/inventory) — the item spec: `name`, `lore`, `count`, `glint`, skins.
- [Canvases and pictures](/wiki/canvases) — the canvas behind a hotbar map.
- [UI basics](/wiki/ui-basics) — the text runs a menu title takes.
