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
| `ui.box{}` | a plain shape | `width`, `height` (1 to 256; 2048 with no `id` and no `radius`), `color`, `radius` |
| `ui.image{}` | a picture | `image` (a `game.texture`), `color` (a tint) |
| `ui.label{}` | words | `text`, `color`, `width`, `align`, `bold` (each letter a pixel wider) |
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
- `ui.define(name, { anchor, margin, child })` takes one child. A layout
is centred across the screen. `anchor` is the edge it hangs from:
  - `"bottom"` (the default): its bottom edge is `margin` pixels above the
screen’s bottom. The default is 40, over the hearts, or 25, just over
the hotbar, when `hide_hud` takes the hearts and the food away.
  - `"top"`: its top edge is `margin` pixels below the screen’s top. The
default is 4. It can reach down the whole screen.
- A plain box (no `id`, no `radius`) is up to 2048 a side: a backdrop
that covers the whole screen at every GUI scale. The game shows through
nowhere it covers. Make the backdrop its own layout (`margin = 0`) and
show it first; then show the menu as a second top layout with its own
`margin`. In one stack the menu would be centred on the backdrop, far
below the bottom of a screen that is 270 pixels tall.
- A top layout is drawn over the crosshair, the hotbar and the hearts, and
under the sidebar, the chat and every bottom layout: a bottom layout can
sit on a top layout’s backdrop.
**A cursor.** `cursor = true` in `ui.define` (a top layout only) puts a
pointer on it that the mouse moves, three pixels a degree, and stops at
the layout’s edges. The view and the head stay still: while it shows, the
player sits on a seat of the engine’s where they stood, and looks out of a
still view at their eyes. Destroying it gives back their feet and eyes.
```luau
local MENU = ui.define("menu", { anchor = "top", margin = 40, cursor = true,
    ui.column{ gap = 4, ui.box{ id = "solo", width = 120, height = 18, color = "#2a3550" },
                        ui.box{ id = "group", width = 120, height = 18, color = "#2a3550" } } })
local m = player.ui.show(MENU)
m.on_hover = function(id) end          -- the id under the pointer changed; nil is none
m.on_click = function(id, button) end  -- a click; id is what is under the pointer, or nil
m.hover                                -- the id under it now
m.cursor                               -- { x, y }: where it is, in the layout's pixels
```
- Only an item with an `id` is found under the pointer, the topmost one.
Give the button’s box the id, not its label: a label is only as tall as
its letters.
- The view looks level, the way the player faced. A player who rides
something or looks out of a camera keeps it: their view then turns with
the mouse.
- The pointer moves as each turn the client sends arrives: 20 times a
second, evenly.
- `players.on_click` still fires for the same click.
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
- A bottom layout uses the action bar. While one shows,
`player.ui.actionbar` text is replaced by it within a second.
- A top layout uses a boss bar of the engine’s. A pack’s own boss bar made
before it shows above it and moves it 19 pixels down; make pack bars
after `player.ui.show`, or not at all on that screen.
- At the bottom a label starts at most 73 pixels up; at the top at least
2 down. A label uses the letters from space to `~`. Any other letter
shows as `?`.
- A layout holds 254 items. A live box or picture is at most 256 wide.
**The game’s own HUD.** `hide_hud` in `citadel.yml` takes parts of it off
the screen, for the whole server and clients from 1.21.4:
```yaml
hide_hud: [hearts, food, armor, air, xp, hotbar, crosshair, dialog_warning, menu_blur, menu_background]    # any of these
resource_pack: required    # or a player without the pack sees no hearts and no layout
```
`xp` hides the bar; the level’s number stays. `hotbar` hides the frame; the
items stay. `menu_blur` and `menu_background` take the blur and the dark
shade from behind every screen opened in the world (a dialog, a chest, the
pause menu), for clients from 1.21.6: the world shows sharp round a
dialog, as round a panel of your own. `dialog_warning` hides the ⚠ that the client puts next to the
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
as unchecked. `--words labels.json` leaves the labels out of the picture
and writes each one’s words, place (`x`, `y` from the picture’s corner),
`width`, `align` and `color` to the file, for a tool that has the
client’s letters.
