---
title: Screens and layouts
section: ui
order: 2
description: world.screen — a wall or floor of map frames drawn on pixel by pixel, with click hooks and per-player views — and the layout system that puts a HUD of boxes, images and labels on the client's own screen.
tags: [ui, screens, pictures, layouts, hud, on-click]
---

# Screens and layouts

> **In short:** a screen is a wall or floor of item frames that hold maps —
> 128 pixels per frame, on every client from 1.8 — that the script draws on
> pixel by pixel, with a click hook and an optional per-player layer. A layout
> is the other direction: a HUD made of boxes, pictures and labels that the
> client itself draws from the resource pack, with live values the script
> changes while it runs. Both belong to their room and end with the script.

## Placing a screen

Put it in the air blocks in front of a wall. [`world.screen{}`](/ref/World/screen)
places it:

| Option            | What it is                                                                       |
| ----------------- | -------------------------------------------------------------------------------- |
| `at`              | The top-left frame as the viewer sees it                                         |
| `facing`          | The side the viewer stands on; `"up"` lies the screen flat                       |
| `up`              | For `facing = "up"`: the way the top of the picture points, `"north"` by default |
| `width`, `height` | The screen's size in frames                                                      |
| `glow`            | `true` makes glow frames on 1.17 and later, plain frames before                  |
| `on_click`        | A click hook, settable here or later                                             |

- Changes go out once per tick, as each frame's box of changed pixels.
- Colours snap to the map palette (about 250 tones). Each client gets its
  closest tone; `color.nearest(c)` does that snap in advance.
- A screen belongs to its room and ends with the script. Players who join
  later see the current picture.

## Drawing on a screen

A screen draws with the [`Picture`](/ref/Picture) calls — the same calls a
canvas or a view takes:

```luau
local board = world.screen{ at = vec3(-2, 68, -10), facing = "south", width = 4, height = 2 }
board.width, board.height                  -- pixels: 512, 256
board:clear(colors.black)                  -- every pixel; default black
board:set(x, y, color)                     -- one pixel, (0, 0) top-left
board:fill(x, y, w, h, color)
board:rect(x, y, w, h, color, 12)          -- rounded corners of radius 12, smoothed
board:circle(x, y, r, color)
board:text(x, y, "Jackpot 2500", colors.yellow, 32)   -- 32 pixels tall, smoothed; returns the width
board:measure("Jackpot 2500", 32)          -- the width without drawing, for centring
board:line(x0, y0, x1, y1, color, 3)       -- 3 pixels wide (1 by default), round ends, smoothed
board:ring(x, y, r, color, 2)              -- a circle's outline, 2 pixels wide (1 by default)
board:polygon({ {10, 10}, {60, 10}, {35, 50} }, color)   -- filled, any number of corners, smoothed
board:gradient(x, y, w, h, colors.red, colors.blue)      -- top to bottom; a 7th value "across" runs left to right
board:sprite(x, y, { ".##.", "#..#", ".##." }, { ["#"] = colors.black }, 4)   -- pixel art, 4 pixels a dot
board:pixels(x, y, w, h, data)             -- raw RGB bytes (a buffer or a string), three a pixel, row by row
board:draw(canvas, x, y)                   -- another canvas or screen, its top-left at (x, y); its transparent pixels are skipped
board:part(col, row)                       -- one map of it, { id = .. }, for a hand or a single frame
board:play{ file = "video/intro.rgb", fps = 20, loop = true }   -- a video; see "video" in Canvases
board:destroy()
```

Text is DejaVu Sans Bold, anti-aliased, 16 pixels by default. It has every
Latin letter, digits, symbols and `♠ ♥ ♦ ♣`.

Drawing notes:

- `line`, `ring` and `polygon` take fractional positions and blend into the
  pixels under them. Draw them on a background, not on `colors.transparent`.
- A polygon point is `{x, y}` or `{ x = .., y = .. }`.
- Each `sprite` string is a row. Each character is a dot `scale` pixels square
  (1 by default). A character with no colour (the `.` above) leaves its pixels
  unchanged.

## Clicks

Set `on_click` (in `world.screen{}` or later) to get the pixel a player clicks:

```luau
board.on_click = function(player, x, y, button)   -- button "left" or "right"
    board:circle(x, y, 6, colors.red)
end
board.on_click = nil   -- no hook again; false does the same
```

- A click on a block or the air behind the picture also counts.
- `players.on_click` still gets the click, with the frame's `entity_id` and no
  handle.

## One player's own layer

`board:view(player)` is one player's own layer over the screen, with the same
drawing calls. Only that player receives it.

```luau
local mine = board:view(player)
mine:text(8, 8, "Your turn", colors.yellow, 24)   -- nobody else sees this
mine:destroy()                                     -- back to the shared picture
```

- See-through pixels show the shared picture. A new view is all see-through,
  and `view:clear()` paints see-through.
- The call returns the same view until `view:destroy()` or the player leaves
  the room.
- Canvases have views too.

## Floor screens

For a floor or a table, set `facing = "up"`, in the air blocks on top.

- `up` is the way the top of the picture points, `"north"` by default. Use
  `"south"` for a player north of the table.
- Rows run away from `up`. With `up = "south"`, x runs west and y runs north.

> **Gotcha:** clients before 1.13 see nothing of a floor screen (the
> `floor_frame` feature).

```luau
local felt = world.screen{ at = vec3(2, 66, 2), facing = "up", up = "south", width = 5, height = 3 }
```

## Layouts

A layout is a HUD made of boxes, pictures and labels: a health bar, a level
badge, a frame round the hotbar. Define it while the pack loads, then show it
to a player and change its values.

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

## The layout tree

Three things to show, three ways to place them:

| Call                            | What it is                                    | Options                                         |
| ------------------------------- | --------------------------------------------- | ----------------------------------------------- |
| [`ui.box{}`](/ref/Ui/box)       | A plain shape                                 | `width`, `height` (1 to 256), `color`, `radius` |
| [`ui.image{}`](/ref/Ui/image)   | A picture                                     | `image` (a `game.texture`), `color` (a tint)    |
| [`ui.label{}`](/ref/Ui/label)   | Words                                         | `text`, `color`, `width`, `align`               |
| [`ui.row{}`](/ref/Ui/row)       | Its children side by side                     | `gap`, `align`, then the children               |
| [`ui.column{}`](/ref/Ui/column) | Its children under each other                 | `gap`, `align`, then the children               |
| [`ui.stack{}`](/ref/Ui/stack)   | Its children over each other, the last on top | `align`, then the children                      |

- There are no coordinates. Rows, columns and stacks place everything. `gap` is
  the pixels between two children. `align` is `"start"`, `"center"` (the
  default) or `"end"`, across the row or column.
- A pixel is one pixel of the game's own HUD: the hotbar is 182 wide and 22
  high.
- A bar is two boxes in a stack. The one with an `id` gets a fill.
- A label is as wide as its first words. Give a label whose words change a
  `width`: its place is fixed when the pack loads.
- [`ui.define(name, { anchor, margin, child })`](/ref/Ui/define) takes one
  child. `anchor` is `"bottom"`: the layout is centred over the hotbar, its
  bottom edge `margin` pixels above the screen's bottom. The default is 40,
  over the hearts, or 25, just over the hotbar, when `hide_hud` takes the
  hearts and the food away.

## Live values

An item with an `id` is live. [`hud:set{}`](/ref/Hud/set) takes a value per id,
and `hud.<id>` has the same values as fields:

| Field     | In `hud:set{}`    | What it is                                                     |
| --------- | ----------------- | -------------------------------------------------------------- |
| `fill`    | a number          | How much of a box or picture shows, from its left edge, 0 to 1 |
| `text`    | a string          | A label's words                                                |
| `visible` | `true` or `false` | Whether it shows; `hud.<id>.visible = nil` shows it again      |
| `color`   | (field only)      | A box's colour, a picture's tint, a label's ink                |

An unknown id is an error that lists the layout's ids. The values tween, as the
`hud.hp` example above shows.

## What is fixed when the pack loads

A client gets the resource pack when it joins, and never again. So the shape,
size, picture and place of every item are fixed when the pack loads, and
`ui.define` in a callback is an error. Show different layouts to different
players; do not look for a way to change one.

## Client support

- Only Java clients from 1.21.4 with the resource pack draw a layout
  (`player:supports("layout")`). On any other client, [`player.ui.show`](/ref/PlayerUi/show)
  returns a handle that takes every call and shows nothing. Send that player
  `player.ui.actionbar` instead. A client that turns the pack down stops
  getting its layouts.
- A layout uses the action bar. While one shows, `player.ui.actionbar` text is
  replaced by it within a second.
- A label starts at most 73 pixels above the screen's bottom, and uses the
  letters from space to `~`. Any other letter shows as `?`.
- A layout holds 254 items. A live box or picture is at most 256 wide.

## The game's own HUD

`hide_hud` in `citadel.yml` takes parts of it off the screen, for the whole
server and clients from 1.21.4 — `hearts`, `food`, `armor`, `air`, `xp`,
`hotbar`, `dialog_warning`:

- `xp` hides the bar; the level's number stays.
- `hotbar` hides the frame; the items stay.
- `dialog_warning` hides the ⚠ that the client puts next to the title of every
  dialog from this server. That sign tells a player the screen is the server's,
  not the game's, so hide it only for screens no one could mistake for the
  game's own.

`resource_pack: required` makes the pack required — or a player without the
pack sees no hearts and no layout. See
[Server settings](/wiki/server-settings).

## Rendering a layout with no client

`citadel ui render` draws a layout with no client:

```sh
citadel ui render ./pack                 # every layout: its size and its ids
citadel ui render ./pack status --out hud.png --set hp=0.5 --set "hp_text=10 / 20" --scale 6
```

Boxes and pictures are exact. A label is drawn as blocks as wide as its
letters, because the letters are the client's own: report a label's words as
unchecked.

## See also

- [Canvases and pictures](/wiki/canvases) — canvases, the shared drawing calls in depth, video and streams.
- [UI basics](/wiki/ui-basics) — the action bar a layout replaces, and the text system.
- [Dialogs](/wiki/dialogs) — full-screen dialogs, also client-drawn and pack-gated.
- [Client versions](/appendix/client-versions) — the `floor_frame`, `glow_frame` and `layout` rows.
- [Server settings](/wiki/server-settings) — `hide_hud` and `resource_pack: required`.
