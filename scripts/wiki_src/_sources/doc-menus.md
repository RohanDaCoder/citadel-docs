# SOURCE: Menus

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

The rules:

- **Every client draws a menu.** Java (1.7 to 26.3) shows a chest. Bedrock shows a form with one button per item, labelled with `name` or the item’s name. No `player:supports` check is needed.
- An item is an item (see “items”) with `name`, `lore`, `color`, `dye`, `glint`, `skin` and `count`. The count shows on the stack, for a price or a quantity.
- `on_pick` may `task.wait`.
  - On Java the menu stays open. Destroy it in `on_pick` if one pick is enough.
  - A Bedrock form closes on the press. Open it again for another pick.
- `menu:destroy()` and a Bedrock pick do not fire `on_close`.
- `menu:update` returns `false` after the player closes the menu. Picks still answer by position. A Bedrock form keeps its first items.
- A new menu replaces the old one.
- Only the pack that opened a menu gets its picks. The menu ends when the script ends, the player leaves, or the pack calls `destroy`.
- Under a Java menu, the player’s inventory shows. Clicks in it change nothing.
