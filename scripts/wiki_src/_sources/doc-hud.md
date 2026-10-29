# SOURCE: HUD

```luau
player.ui.actionbar("Bet 50 · Chips 1200", "light_purple")    -- the line above the hotbar
local bar = ui.bossbar{ title = "Race starts in 30 s", color = "purple", progress = 1 }
bar.title, bar.progress, bar.color, bar.visible    -- live; progress 0..1
bar.visible = false    -- off every screen; true or nil shows it again a bar's colour is its own closed set: pink, blue, red, green, yellow, purple, white. It is not a colour value and has no hex form; anything else is white. While a layout hangs from the top (see "Layouts"), pink is the engine's, and a pink bar is an error.
bar:destroy()
local mine = player.ui.bossbar{ title = "Your horse: Lightning" }    -- one player's bar, the same handle
ui.sidebar{ title = "INDIGO", lines = { "Chips 1200", "Bet 50", "", "Roulette" } }    -- everyone in the room
player.ui.sidebar{ title = "INDIGO", lines = { ... } }    -- one player; lines run top to bottom
ui.sidebar(false)    -- removes the sidebar, as nil does; player.ui.sidebar(false) for one player
ui.tab{ header = "INDIGO", footer = "minefort.com" }    -- every title, line, header and footer here is text: { "Chips ", { "1200", color = "gold" } }
```
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
