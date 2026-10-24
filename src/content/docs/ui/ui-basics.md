---
title: 'UI basics'
description: 'Chat lines, titles and subtitles, the action bar, boss bars, the sidebar and the tab list — the ui global and player.ui — plus the text-run system, colour names and moving text that every text surface shares.'
---

:::note[In short]
the text surfaces of a player's screen — chat, titles, the
action bar, boss bars, the sidebar and the tab list. The `ui` global (or
`room.ui`) addresses everyone in a room; `player.ui` holds the same calls for
one player. Every call takes the same text: a string, a table of styled runs,
or a function of the time. The run syntax, the colour spellings and the
moving-text rules are documented here once and used by every other surface.
:::

## One set of calls, everyone or one player

Titles, chat, the action bar, boss bars, the sidebar and the tab list are one
family of calls. `ui` (or `room.ui`) reaches everyone in a room; `player.ui`
holds the same calls for one player — "everyone" below is one player on
`player.ui`.

| Call | Returns | Purpose |
| --- | --- | --- |
| [`ui.title{ title, subtitle, color, fade_in, stay, fade_out }`](/ref/Ui/title/) | — | Title and subtitle; fades and stay in seconds |
| [`ui.actionbar(text, color?)`](/ref/Ui/actionbar/) | — | The line above the hotbar |
| [`ui.bossbar{ title, color, progress }`](/ref/Ui/bossbar/) | `Bar` | A boss bar; progress 0..1 |
| [`ui.sidebar{ title, lines }`](/ref/Ui/sidebar/) | — | The sidebar; `nil` or `false` removes it |
| [`ui.tab{ header, footer }`](/ref/Ui/tab/) | — | The tab list's header and footer |
| [`message(text, color?)`](/ref/message/) | — | A chat line to everyone in the main room |
| [`player:message(text, color?)`](/ref/Player/message/) | — | A chat line to this player alone |

## Chat lines

Chat is not part of the screen, so it is not in `ui`. `message(text, color)`
sends a chat line to everyone in the main room; `player:message(text, color)`
sends one to a single player. In both, `color` is for the words that did not
pick a colour of their own.

## Titles and subtitles

```luau
ui.title{ title = "DROP", subtitle = "hands up", color = "red",
    fade_in = 0.1, stay = 0.7, fade_out = 0.4 }   -- fades and stay are in seconds
```

`title` and `subtitle` are text (see [Text runs](#text-runs)); the call's
`color` colours the words with no colour of their own.

## The action bar

```luau
ui.actionbar("Round 2", "gold")                            -- everyone in the room
player.ui.actionbar("Bet 50 · Chips 1200", "light_purple") -- one player
```

The line above the hotbar; the call's `color` is for the words that did not
pick one.

## Boss bars

```luau
local bar = ui.bossbar{ title = "Race starts in 30 s", color = "purple", progress = 1 }
bar.title, bar.progress, bar.color, bar.visible   -- live; progress 0..1
bar.visible = false    -- off every screen; true or nil shows it again
bar:destroy()
local mine = player.ui.bossbar{ title = "Your horse: Lightning" }   -- one player's bar, the same handle
```

The [`Bar`](/ref/Bar/) handle's live fields:

| Field | What it is |
| --- | --- |
| `bar.title` | Reads back the words; takes any text |
| `bar.progress` | How full the bar is, 0 to 1 |
| `bar.color` | From the bar's own closed set; anything else is white |
| `bar.visible` | `false` takes it off every screen; `true` or `nil` shows it again |

A boss bar needs the `bossbar` feature: clients from 1.9.

:::caution[Gotcha]
1.8 has no boss bars. A 1.8 client shows the title on its action
bar.
:::

A bar's colour is its own closed set: `pink`, `blue`, `red`, `green`, `yellow`,
`purple`, `white`. It is not a colour value and has no hex form; anything else
is white.

:::note
a boss bar re-sends on every change. A late joiner sees it at the
next change.
:::

## The sidebar

```luau
ui.sidebar{ title = "INDIGO", lines = { "Chips  1200", "Bet  50", "", "Roulette" } }  -- everyone in the room
player.ui.sidebar{ title = "INDIGO", lines = { ... } }   -- one player; lines run top to bottom
ui.sidebar(false)     -- removes the sidebar, as nil does; player.ui.sidebar(false) for one player
```

:::caution[Gotcha]
the sidebar sends only changed lines. Repeated lines are fine;
long or extra lines are trimmed.
:::

## The tab list

```luau
ui.tab{ header = "INDIGO", footer = "minefort.com" }
```

Sets the player list's header and footer. Every title, line, header and footer
on this page is text: `{ "Chips ", { "1200", color = "gold" } }`.

## Text runs

Every call that shows words takes text: chat, the action bar, titles, kicks,
boss bars, the sidebar, the tab header and footer, item name and lore, menu
titles, text displays, npc speech and name tags. Text is a string or a table:

```luau
"Lap 2/3"                                                   -- words, in the surface's own colour
{ "1st", color = colors.gold, bold = true }                 -- one styled run
{ "Lap ", { "2", color = "white", bold = true }, "/3", color = "gray" }
player.ui.sidebar{ title = { "KART", color = "gold", bold = true }, lines = {
    { { "1. ", color = "yellow" }, "Mario" },
    { "2. Luigi", color = color(0.4, 1, 0.4) },
} }
```

- A table's entries are its **runs**: strings or tables.
- Its named fields style all its runs: `color`, `bold`, `italic`, `underline`,
  `strike`. A run's own style wins.
- A call's own colour (`player:message(text, color)`, `ui.actionbar(text, color)`,
  a title's `color`, a text display's `color`, `npc:say(text, color)`) colours
  the words with no colour.
- A live text field (`bar.title`, a display's `text`) reads back the words.

:::caution[Gotcha]
any other field is an error that names the five style fields.
:::

## Text that moves

A text table's `effect` styles **every letter**. A whole text can also be a
**function of the time**.

- The sidebar, boss bars, the tab list and text displays recompute them ten
  times a second. Other surfaces show the frame at send time.
- Only what moves is recomputed: a sidebar's still lines are read when it is
  set. To change one, set the sidebar again.
- A moving text table shown to many players at once, such as one title table
  every player's sidebar uses, is worked out once a frame.

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

An effect returns a style (`color`, `bold`, `italic`, `underline`, `strike`,
plus `text` to replace the letter, `""` to hide it) or `nil`. More effects,
each one line:

```luau
-- colours across the letters, flowing at `speed` cycles a second
function(_, i, n, t) return { color = color.gradient(list, (i - 1) / n - t * speed, true) } end
-- the whole text in one colour at a time, `speed` times through the list a second
function(_, _, _, t) return { color = list[math.floor(t * speed * #list) % #list + 1] } end
-- the letters appear one after another, `rate` a second from `from = time.now()`
function(_, i, _, t) if i > (t - from) * rate then return { text = "" } end end
```

:::caution[Gotcha]
an effect or text function that errors keeps its last frame and
logs why.
:::

:::caution[Gotcha]
clients from 1.16 get exact colours, older ones the nearest of the
sixteen. Sidebar lines take hex colours from 1.20.3. A screen or canvas draws
text as pixels, in the colour of its `text` call — see
[Screens and layouts](/ui/screens/).
:::

## Colour names and helpers

Anywhere a colour is asked for, every spelling works: a `color` value, a name,
or hex (`"#ff8800"`). A name nobody has is an error that says the nearest.

| Set | Names |
| --- | --- |
| Minecraft's sixteen, every client since 1.7 | `black`, `dark_blue`, `dark_green`, `dark_aqua`, `dark_red`, `dark_purple`, `gold`, `gray`, `dark_gray`, `blue`, `green`, `aqua`, `red`, `light_purple`, `yellow`, `white` |
| Six more | `orange`, `lime`, `cyan`, `purple`, `magenta`, `pink` |
| Special | `transparent` |

`colors` holds the same names as values; any other name is an error naming the
nearest (`colors.grey` says `gray`).

| Helper | What it does |
| --- | --- |
| `color(r, g, b)` | A colour from red, green and blue, each 0 to 1 |
| `color.hsv(h, s, v)` | From hue, saturation and value, each 0 to 1 |
| `color.gradient(list, u, loop?)` | The colour `u` (0 to 1) of the way along the list; with `loop`, `u` wraps and the last colour runs back into the first |
| `color.nearest(c)` | The colour a picture really shows, since a picture snaps to the map palette |
| `kit.mix(a, b, t)` | Mixes two `"#rrggbb"` colours (see [Dialogs](/ui/dialogs/)) |

## A canvas on the player's screen

`player.ui.overlay` puts a 128×128 canvas in a corner of one player's screen.
It draws like a canvas. Only that player sees it.

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

- `corner` is `top_left`, `top_right`, `bottom_left` or `bottom_right`. `size`
  is screen pixels a side at GUI scale 1 (16 to 511). `margin` is the gap to
  the edges (0 to 63). The client's automatic GUI scale multiplies both.
- It stays over room moves and respawns. It goes when the player leaves.
- Changed pixels go to that player once per tick.
- Only 26.3 draws it, with the engine's shader in the resource pack. A pack
  that names `player.ui.overlay` makes the pack required for 26.3; a player
  who declines it is disconnected with a how-to message.
- Several at once are fine: each is its own canvas.

:::caution[Gotcha]
shader mods (Iris, OptiFine) replace the shader. There the HUD
does not show.
:::

## See also

- [Screens and layouts](/ui/screens/) — pixel screens and client-drawn HUD layouts.
- [Canvases and pictures](/ui/canvases/) — the canvas drawing calls the overlay shares, video and streams.
- [Conventions](/concepts/conventions/) — colour, text and options-table rules across the API.
- [Client versions](/appendix/client-versions/) — the per-feature version matrix (`bossbar` 1.9, `overlay` 26.3).
- [Leaderboards cookbook](/cookbook/cookbook-leaderboards/) — a sidebar in use.
