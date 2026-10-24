# SOURCE: Screens

- Put it in the air blocks in front of a wall.
- `at` is the top-left frame as the viewer sees it.
- `facing` is the side the viewer stands on.
- Changes go out once per tick, as each frame’s box of changed pixels.
- Colours snap to the map palette (about 250 tones). Each client gets its
  closest tone.
- `color.nearest(c)` does that snap in advance.
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
