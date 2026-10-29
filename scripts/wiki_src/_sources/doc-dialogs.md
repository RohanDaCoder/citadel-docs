# SOURCE: Dialogs

```luau
local kit = ui.kit

local function servers(player)
    local tab = 1
    local d = player.ui.dialog(function()           -- a function: drawn again after every click
        return kit.window{
            title = "Servers", size = "screen", button = false,
            kit.tabs{ "Featured", "Popular", selected = tab, on_change = function(p, i) tab = i end },
            kit.grid{ columns = 3,
                kit.card{ image = "https://example.org/carball.png", title = "Carball", text = "by Melvin",
                    badges = { kit.badge{ "LIVE", color = kit.theme.live, dot = true } },
                    on_click = function(p) p:message("Joining Carball") end },
            },
            kit.row{ justify = "end", kit.close() },
        }
    end)
    if not d then player.ui.menu{ title = "Servers", items = { "slime_ball" }, on_pick = function() end } end
end
```
A pack that opens dialogs says so in its `citadel.yml`, so their fonts are
in the resource pack from the first join:
```yaml
dialogs: true
```
Without it, `player.ui.dialog` is an error that names the line to add.
`player.ui.dialog(view)` takes a `ui.kit.window{}`, or a function that
returns one. With a function the dialog is live: after every click it
calls the function again and draws what it returns, so a click only has to
change your state. It returns a handle:
- `d:refresh()` draws a live view again (after a change that was not a click).
- `d:update(view)` puts a new view (a window or a function) in place.
- `d:destroy()` closes it. `d.open` is `false` once the player closed it.
`ui.kit` is what a dialog is made of. Six primitives the engine draws, each
a table you can also write by hand:
- `kit.row{ ... }`, `kit.column{ ... }`, `kit.stack{ ... }` (children on top
of each other): the children are the list part. Keys: `gap`, `pad` (a
number, `{ y, x }` or `{ top, right, bottom, left }`), `align` and
`justify` (`"start"`, `"center"`, `"end"`, and `"stretch"` or
`"between"`), `fill` and `fill_to` (a gradient), `border`,
`border_width`, `radius`, `shadow` (0 to 8). A root box may also set
`edge_glyph = "namespace:name"` to paint that pack glyph behind the body
and across the native widget’s padding; the body retains its own hit boxes.
Alternatively, `bleed = true` on the root lets its children occupy the
widget’s padding itself, for artwork that must meet the dialog edges.
- `kit.space{}`: an empty box that takes `width`, `height` or `grow`.
- `kit.text("Hi")` or `kit.text{ "Hi", color = ..., bold = true, shadow = false, align = "center" }`.
`font_size` selects a native bitmap font height from 2 to 16 GUI pixels
(default 8). `tracking` adjusts the advance between letters by -1 to 4
GUI pixels (default 0). The engine uses the same metrics to fit the text.
`font = "namespace:heading"` selects a pack-authored bitmap typeface; its
declared ink height replaces `font_size`. Labels stay anchored at their
top edge, including when layered over image-backed controls.
- `kit.image{ image = ..., radius = 4, detail = 2 }`: `image` is an
`https://` URL (fetched once by the engine), a PNG or WebP file in the
pack, or a `game.texture`; `detail = 2` has four times the pixels. Set
`pixel_art = true` to use nearest-neighbor sampling and preserve exact
colors for small pixel art such as player avatars.
Use `kit.image{ glyph = "name" }` for one of the pack’s own glyphs. A picture
still on its way shows a placeholder, and the dialog is drawn again when
it arrives.
Every node also takes `width`, `height`, `grow`, `on_click` (a
`function(player)`, or `"close"`) and `hover` (words shown under the
pointer).
Pack-authored typefaces live in `assets/<namespace>/dialog-fonts/<name>.json`:
```json
{
  "source": "font/heading.png",
  "cell": [36, 60],
  "chars": ["ABCDEFGHIJKLMNOPQRSTUVWXYZ?"],
  "density": 6,
  "spacing": -0.5,
  "space": 2,
  "advances": { "A": 3.5, "I": 1.5 }
}
```
The PNG lives under the namespace’s `textures` directory. Each character
uses one cell, in row order; `\u0000` skips a cell and `?` is required as a
fallback. Draw white ink at the cell’s top left on transparency; `color`
tints it at runtime. Every row must have the same number of cells. `density`
is source texels per GUI pixel (1–8). Cell height must be divisible by density
and at least eight GUI pixels, with extra transparent rows under small ink.
Both cell dimensions must fit a 256-texel native font atlas page. `spacing`
is -1 to 4 GUI pixels, added between characters; `space` is the native space
advance (1–16 GUI pixels). Optional `advances` supplies authored layout
advances per character, including spaces, as finite numbers from 1 to 64 GUI
pixels. These replace the rounded bitmap advance plus `spacing`. The engine
accumulates fractional advances and places each glyph to the nearest 1/64
GUI pixel, keeping layout, clipping, previews and packets consistent.
Font changes require a resource-pack rebuild and reconnect.
For high-resolution artwork, put a JSON atlas beside glyph PNGs at
`assets/<namespace>/textures/glyph/atlas.json`:
```json
{
  "source": "browser.png",
  "density": 5,
  "sprites": {
    "browser": { "rect": [0, 0, 1672, 941] },
    "join": { "rect": [1248, 805, 380, 76], "offset": [3, 0] }
  }
}
```
`source` is relative to that namespace’s `textures` directory and must stay
inside it. `rect` is `[x, y, width, height]` in source texels; `density` is
1 to 8 source texels per GUI pixel. The engine preserves the source pixels,
pads incomplete GUI pixels transparently, and splits large sprites into
tiles that fit Minecraft’s 256-pixel font atlas pages. Existing glyph PNGs
keep their two-texel density. Use `kit.image{ glyph = "namespace:join" }`.
Optional `offset = [x, y]` adds fewer than `density` transparent texels before
the crop to align artwork to its source grid. `size = [width, height]`
resizes a texture strip with nearest-neighbor sampling. Optional `patches`
is a list of `{ "source": [x,y,w,h], "target": [x,y,w,h] }` crops from the
same source image, composited into the sprite in order; targets are relative
to its unpadded output. This supports textured button and card variants.
Optional `ink_mask` extracts lettering onto transparency: `"light"` keeps
pixels with RGB channels above `[180, 180, 140]`; `"dark"` keeps pixels below
`[100, 80, 70]`. With a mask, `tint = [r, g, b]` recolors the retained ink.
This lets a label be layered over different button backgrounds without
bringing its old background along.
Atlas changes require a new resource pack and reconnect; Luau state changes
and text updates do not.
Use `kit.stack` to layer images, text, and controls in child order, from back
to front. Transparent glyph texels preserve the layers underneath. Place
invisible `kit.space{ width, height, on_click }` controls last when their
click rectangles span several visual layers. Their native cursor bounds
match the rectangle, independently of the images’ text baselines.
How an image is drawn: one `width = 144, height = 80` directly in
`kit.window`, or first in a `kit.row` directly in it (the row’s other
children sit beside it), is one picture the client renders once, so it is
cheap. Only the first such image in a window is drawn this way; every other
image is drawn in glyph cells, which the client draws every frame.
Made of those, in plain Luau (copy one to make your own): `kit.window{ title, button, on_close, input, size = "screen", ... }` (the dialog;
`button` is its button’s label, `false` for none; `input = { label, value, width, on_submit = function(player, text) end }` adds a text field;
`size = "screen"` is `kit.SCREEN`, a body that fits every screen without a
scrollbar), `kit.button{ "Play", style = "primary" | "secondary" | "ghost" | "danger", on_click }`, `kit.tabs{ "A", "B", selected, on_change }`,
`kit.close{}`, `kit.badge{ "LIVE", color, dot }`, `kit.dot{}`,
`kit.progress{ value = 0.5 }`, `kit.divider{}`, `kit.card{ image, title, text, badges, on_click }` and `kit.grid{ columns = 3, gap = 6, ... }` (any
nodes, in rows of `columns`).
`kit.theme` holds the colours they use when a call names none: change it
once to restyle them all. `kit.theme.shadow` (false) is whether kit text
draws the game’s drop shadow when a call does not say.
A `game.texture` in `kit.image` is pixel art: each pixel grows into a
block of the same colour, and its see-through pixels show the box under
it. Give the image a `width` and `height` that are whole multiples of the
texture’s for even pixels. `kit.mix(a, b, t)` mixes two `"#rrggbb"` colours.
The rules:
- A new dialog replaces the open one. Escape closes it and calls the
window’s `on_close(player)`.
- Clicks may `task.wait`. Only the pack that opened a dialog gets its clicks.
- A player who turned the resource pack down is sent no dialog: it is drawn
in the pack’s fonts.
