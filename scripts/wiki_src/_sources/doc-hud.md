# SOURCE: HUD

- A boss bar re-sends on every change. A late joiner sees it at the next
  change.
- 1.8 has no boss bars. A 1.8 client shows the title on its action bar.
- The sidebar sends only changed lines. Repeated lines are fine. Long or
  extra lines are trimmed.

## A canvas on the screen

`player.ui.overlay` puts a 128×128 canvas in a corner of one player’s
screen. It draws like a canvas. Only that player sees it.

```luau
local map = player.ui.overlay{ corner = "top_right", size = 96, margin = 4 }   -- nil where player:supports("overlay") is false
if map then
    map:clear()                                  -- see-through: the game shows through
    map:rect(0, 1, 128, 127, "#101820", 10)      -- rows 1..127; row 0 is the engine's and never shows
    map:text(8, 6, "MAP", colors.white, 12)
    map.open                                     -- false after destroy or when the player leaves
    map:destroy()
end
```

- `corner` is `top_left`, `top_right`, `bottom_left` or `bottom_right`.
  `size` is screen pixels a side at GUI scale 1 (16 to 511). `margin` is
  the gap to the edges (0 to 63). The client’s automatic GUI scale
  multiplies both.
- It stays over room moves and respawns. It goes when the player leaves.
- Changed pixels go to that player once per tick.
- Only 26.3 draws it, with the engine’s shader in the resource pack. A pack
  that names `player.ui.overlay` makes the pack required for 26.3. A player who
  declines it is disconnected with a how-to message.
- Several at once are fine: each is its own canvas.
- Shader mods (Iris, OptiFine) replace the shader. There the HUD does not
  show.
