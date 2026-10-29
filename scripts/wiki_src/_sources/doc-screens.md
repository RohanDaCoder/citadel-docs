# SOURCE: Screens

- Put it in the air blocks in front of a wall.
- `at` is the top-left frame as the viewer sees it.
- `facing` is the side the viewer stands on.
- Changes go out once per tick, as each frame’s box of changed pixels.
- Colours snap to the map palette (about 250 tones). Each client gets its
closest tone.
- `color.nearest(c)` does that snap in advance.
```luau
local board = world.screen{ at = vec3(-2, 68, -10), facing = "south", width = 4, height = 2 }
board.width, board.height    -- pixels: 512, 256
board:clear(colors.black)    -- every pixel; default black
board:set(x, y, color)    -- one pixel, (0, 0) top-left
board:fill(x, y, w, h, color)
board:rect(x, y, w, h, color, 12)    -- rounded corners of radius 12, smoothed
board:circle(x, y, r, color)
board:text(x, y, "Jackpot 2500", colors.yellow, 32)    -- 32 pixels tall, smoothed; returns the width
board:measure("Jackpot 2500", 32)    -- the width without drawing, for centring
board:line(x0, y0, x1, y1, color, 3)    -- 3 pixels wide (1 by default), round ends, smoothed
board:ring(x, y, r, color, 2)    -- a circle's outline, 2 pixels wide (1 by default)
board:polygon({ {10, 10}, {60, 10}, {35, 50} }, color)    -- filled, any number of corners, smoothed
board:gradient(x, y, w, h, colors.red, colors.blue)    -- top to bottom; a 7th value "across" runs left to right
board:sprite(x, y, { ".##.", "#..#", ".##." }, { ["#"] = colors.black }, 4)    -- pixel art, 4 pixels a dot
board:pixels(x, y, w, h, data)    -- raw RGB bytes (a buffer or a string), three a pixel, row by row
board:draw(canvas, x, y)    -- another canvas or screen, its top-left at (x, y); its transparent pixels are skipped
board:part(col, row)    -- one map of it, { id = .. }, for a hand or a single frame
board:play{ file = "video/intro.rgb", fps = 20, loop = true }    -- a video; see "video" below
board:destroy()
```
- Text is DejaVu Sans Bold, anti-aliased, 16 pixels by default. It has every
Latin letter, digits, symbols and `♠ ♥ ♦ ♣`.
- A screen belongs to its room and ends with the script.
- Players who join later see the current picture.
Set `on_click` (in `world.screen{}` or later) to get the pixel a player
clicks:
```luau
board.on_click = function(player, x, y, button)   -- button "left" or "right"
    board:circle(x, y, 6, colors.red)
end
board.on_click = nil   -- no hook again; false does the same
```
- A click on a block or the air behind the picture also counts.
- `players.on_click` still gets the click, with the frame’s `entity_id` and
no handle.
`board:view(player)` is one player’s own layer over the screen, with the same
drawing calls.
- Only that player receives it.
- See-through pixels show the shared picture. A new view is all
see-through, and `view:clear()` paints see-through.
- The call returns the same view until `view:destroy()` or the player leaves
the room.
- Canvases have views too.
```luau
local mine = board:view(player)
mine:text(8, 8, "Your turn", colors.yellow, 24)    -- nobody else sees this
mine:destroy()    -- back to the shared picture
```
`glow = true` makes glow frames on 1.17 and later, plain frames before. A
glow frame stays bright in a dark room.
Drawing notes:
- `line`, `ring` and `polygon` take fractional positions and blend into the
pixels under them. Draw them on a background, not on `colors.transparent`.
- A polygon point is `{x, y}` or `{ x = .., y = .. }`.
- Each `sprite` string is a row. Each character is a dot `scale` pixels
square (1 by default). A character with no colour (the `.` above) leaves
its pixels unchanged.
For a floor or a table, set `facing = "up"`, in the air blocks on top.
- `up` is the way the top of the picture points, `"north"` by default. Use
`"south"` for a player north of the table.
- Rows run away from `up`. With `up = "south"`, x runs west and y runs
north.
- Clients before 1.13 see nothing of a floor screen.
```luau
local felt = world.screen{ at = vec3(2, 66, 2), facing = "up", up = "south", width = 5, height = 3 }
```
