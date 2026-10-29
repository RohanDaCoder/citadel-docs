# SOURCE: Text formatting

Text is a string or a table:

```luau
"Lap 2/3"                                                   -- words, in the surface's own colour
{ "1st", color = colors.gold, bold = true }                 -- one styled run
{ "Lap ", { "2", color = "white", bold = true }, "/3", color = "gray" }
player.ui.sidebar{ title = { "KART", color = "gold", bold = true }, lines = {
    { { "1. ", color = "yellow" }, "Mario" },
    { "2. Luigi", color = color(0.4, 1, 0.4) },
} }
```

- A table’s entries are its **runs**: strings or tables.
- Its named fields style all its runs: `color`, `bold`, `italic`,
  `underline`, `strike`. A run’s own style wins.
- A call’s own colour (`player:message(text, color)`, `ui.actionbar(text, color)`, a title’s `color`, a text display’s `color`, `npc:say(text, color)`) colours the words with no colour.
- Any other field is an error that names the five style fields.
- A live text field (`bar.title`, a display’s `text`) reads back the words.

## Text that moves

A text table’s `effect` styles **every letter**. A whole text can also be a
**function of the time**.

- The sidebar, boss bars, the tab list and text displays recompute them ten
  times a second. Other surfaces show the frame at send time.
- Only what moves is recomputed: a sidebar’s still lines are read when it is
  set. To change one, set the sidebar again.
- A moving text table shown to many players at once, such as one title
  table every player’s sidebar uses, is worked out once a frame.

```luau
-- a rainbow, one cycle a second: letter, its number i of n, and t = time.now()
local rainbow = function(letter, i, n, t) return { color = color.hsv((i - 1) / n + t, 1, 1) } end
p.ui.sidebar { title = { "KART", effect = rainbow, bold = true } }

local sparkle = function(letter, i, n, t)
    if (i + math.floor(t * 8)) % 4 == 0 then
        return { color = "white", bold = true }
    end
    return { color = "gold" }                -- or nil: the letter as it was
end
world.display { kind = "text", at = vec3(0.5, 70, 0.5), text = { "WINNER", effect = sparkle } }

-- a text that is a function of the time: rebuilt every frame
ui.sidebar { title = "Lobby", lines = {
    function(t) return { "Next race in " .. math.max(0, math.ceil(race_at - t)), color = "yellow" } end,
} }
```

- An effect returns a style (`color`, `bold`, `italic`, `underline`,
  `strike`, plus `text` to replace the letter, `""` to hide it) or `nil`.
- More effects, each one line:
  `-- colours across the letters, flowing at `speed`cycles a second
function(_, i, n, t) return { color = color.gradient(list, (i - 1) / n - t * speed, true) } end
-- the whole text in one colour at a time,`speed`times through the list a second
function(_, _, _, t) return { color = list[math.floor(t * speed * #list) % #list + 1] } end
-- the letters appear one after another,`rate`a second from`from = time.now()`function(_, i, _, t) if i > (t - from) * rate then return { text = "" } end end`
- An effect or text function that errors keeps its last frame and logs why.
  Clients from 1.16 get exact colours, older ones the nearest of the sixteen.
  Sidebar lines take hex colours from 1.20.3.
  A screen or canvas draws text as pixels, in the colour of its `text` call.
