# SOURCE: Layouts

```luau
local STATUS = ui.define("status", { anchor = "bottom", margin = 42,
    ui.row{ gap = 6, align = "end",
        ui.column{ gap = 1,
            ui.label{ id = "hp_text", text = "20 / 20", width = 82 },
            ui.stack{
                ui.box{ width = 82, height = 9, color = "#1c1410", radius = 2 },   -- the frame
                ui.box{ id = "hp", width = 80, height = 7, color = "red", radius = 1 },
            },
        },
        ui.label{ id = "level", text = "1", color = "gold" },
    },
})

players.on_join(function(player)
    local hud = player.ui.show(STATUS)
    hud:set{ hp = 0.7, hp_text = "14 / 20", level = "22" }
    hud.hp.color = "orange"                          -- every value is a live field too
    tween(hud.hp, { fill = 0 }, { duration = 2 })
    player.data.hud = hud                            -- hud:destroy() takes it off the screen
end)
```
**The tree.** Three things to show, three ways to place them:
| call | what it is | options |
| --- | --- | --- |
| `ui.box{}` | a plain shape | `width`, `height` (1 to 256), `color`, `radius` |
| `ui.image{}` | a picture | `image` (a `game.texture`), `color` (a tint) |
| `ui.label{}` | words | `text`, `color`, `width`, `align` |
| `ui.row{}` | its children side by side | `gap`, `align`, then the children |
| `ui.column{}` | its children under each other | `gap`, `align`, then the children |
| `ui.stack{}` | its children over each other, the last on top | `align`, then the children |
- There are no coordinates. Rows, columns and stacks place everything.
`gap` is the pixels between two children. `align` is `"start"`,
`"center"` (the default) or `"end"`, across the row or column.
- A pixel is one pixel of the game’s own HUD: the hotbar is 182 wide and 22
high.
- A bar is two boxes in a stack. The one with an `id` gets a fill.
- A label is as wide as its first words. Give a label whose words change a
`width`: its place is fixed when the pack loads.
- `ui.define(name, { anchor, margin, child })` takes one child. `anchor` is
`"bottom"`: the layout is centred over the hotbar, its bottom edge
`margin` pixels above the screen’s bottom. The default is 40, over the
hearts, or 25, just over the hotbar, when `hide_hud` takes the hearts
and the food away.
**The values.** An item with an `id` is live. `hud:set{}` takes a value per
id, and `hud.<id>` has the same values as fields:
| field | in `hud:set{}` | what it is |
| --- | --- | --- |
| `fill` | a number | how much of a box or picture shows, from its left edge, 0 to 1 |
| `text` | a string | a label’s words |
| `visible` | `true` or `false` | whether it shows; `hud.<id>.visible = nil` shows it again |
| `color` | (field only) | a box’s colour, a picture’s tint, a label’s ink |
An unknown id is an error that lists the layout’s ids.
**What is fixed.** A client gets the resource pack when it joins, and never
again. So the shape, size, picture and place of every item are fixed when
the pack loads, and `ui.define` in a callback is an error. Show different
layouts to different players; do not look for a way to change one.
- Only Java clients from 1.21.4 with the resource pack draw a layout
(`player:supports("layout")`). On any other client, `player.ui.show`
returns a handle that takes every call and shows nothing. Send that player
`player.ui.actionbar` instead. A client that turns the pack down stops
getting its layouts.
- A layout uses the action bar. While one shows, `player.ui.actionbar` text
is replaced by it within a second.
- A label starts at most 73 pixels above the screen’s bottom, and uses the
letters from space to `~`. Any other letter shows as `?`.
- A layout holds 254 items. A live box or picture is at most 256 wide.
**The game’s own HUD.** `hide_hud` in `citadel.yml` takes parts of it off
the screen, for the whole server and clients from 1.21.4:
`xp` hides the bar; the level’s number stays. `hotbar` hides the frame; the
items stay. `dialog_warning` hides the ⚠ that the client puts next to the
title of every dialog from this server: that sign tells a player the screen
is the server’s, not the game’s, so hide it only for screens no one could
mistake for the game’s own.
**Look at it.** `citadel ui render` draws a layout with no client:
```sh
citadel ui render ./pack                 # every layout: its size and its ids
citadel ui render ./pack status --out hud.png --set hp=0.5 --set "hp_text=10 / 20" --scale 6
```
Boxes and pictures are exact. A label is drawn as blocks as wide as its
letters, because the letters are the client’s own: report a label’s words
as unchecked.
