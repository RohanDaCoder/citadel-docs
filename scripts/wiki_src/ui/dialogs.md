---
title: Dialogs
section: ui
order: 5
description: player.ui.dialog — a screen of boxes, words and pictures built from ui.kit, live-redrawn after every click. Needs Java 1.21.6, a declared dialogs flag in citadel.yml, and a client that took the resource pack.
tags: [ui, dialogs, kit, windows, forms]
---

# Dialogs

> **In short:** a dialog is a screen of boxes, words and pictures over the
> player's view: a server list, a shop, a page of rules. It needs Java 1.21.6
> or newer (`player:supports("dialog")`); on any other client `player.ui.dialog`
> answers `nil`, so give those players a menu or chat instead. Dialogs are
> built from `ui.kit` nodes — plain tables — and a function view makes the
> dialog live: it is drawn again after every click.

## Opening a dialog

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

## Declaring dialogs in `citadel.yml`

A pack that opens dialogs says so in its `citadel.yml`, so their fonts are in
the resource pack from the first join:

```yaml
dialogs: true
```

Without it, `player.ui.dialog` is an error that names the line to add.

## The dialog handle

[`player.ui.dialog(view)`](/ref/PlayerUi/dialog) takes a `ui.kit.window{}`, or
a function that returns one. With a function the dialog is live: after every
click it calls the function again and draws what it returns, so a click only
has to change your state. It returns a handle:

| Call or field    | What it does                                                  |
| ---------------- | ------------------------------------------------------------- |
| `d:refresh()`    | Draws a live view again (after a change that was not a click) |
| `d:update(view)` | Puts a new view (a window or a function) in place             |
| `d:destroy()`    | Closes it                                                     |
| `d.open`         | `false` once the player closed it                             |

The view itself is a [`DialogNode`](/ref/DialogNode): a table with a `kind`,
made by `ui.kit` — or written by hand.

## `ui.kit`: the six primitives

`ui.kit` is what a dialog is made of. Six primitives the engine draws, each a
table you can also write by hand:

- `kit.row{ ... }`, `kit.column{ ... }`, `kit.stack{ ... }` (children on top of
  each other): the children are the list part. Keys: `gap`, `pad` (a number,
  `{ y, x }` or `{ top, right, bottom, left }`), `align` and `justify`
  (`"start"`, `"center"`, `"end"`, and `"stretch"` or `"between"`), `fill` and
  `fill_to` (a gradient), `border`, `border_width`, `radius`, `shadow` (0 to 8).
- `kit.space{}`: an empty box that takes `width`, `height` or `grow`.
- `kit.text("Hi")` or `kit.text{ "Hi", color = ..., bold = true, shadow = false, align = "center" }`.
- `kit.image{ image = ..., radius = 4, detail = 2 }`: `image` is an `https://`
  URL (fetched once by the engine), a PNG or WebP file in the pack, or a
  `game.texture`; `detail = 2` has four times the pixels. Or
  `kit.image{ glyph = "name" }` for one of the pack's own glyphs. A picture
  still on its way shows a placeholder, and the dialog is drawn again when it
  arrives.

Every node also takes `width`, `height`, `grow`, `on_click` (a
`function(player)`, or `"close"`) and `hover` (words shown under the pointer).

> **Gotcha:** how an image is drawn — one `width = 144, height = 80` directly
> in `kit.window`, or first in a `kit.row` directly in it (the row's other
> children sit beside it), is one picture the client renders once, so it is
> cheap. Only the first such image in a window is drawn this way; every other
> image is drawn in glyph cells, which the client draws every frame.

## Composed nodes

Made of the primitives, in plain Luau (copy one to make your own):

| Node                                                                 | What it is                                                                                                                                                                                                                                             |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `kit.window{ title, button, on_close, input, size = "screen", ... }` | The dialog itself. `button` is its button's label, `false` for none; `input = { label, value, width, on_submit = function(player, text) end }` adds a text field; `size = "screen"` is `kit.SCREEN`, a body that fits every screen without a scrollbar |
| `kit.button{ "Play", style = ..., on_click }`                        | A button; `style` is `"primary"`, `"secondary"`, `"ghost"` or `"danger"`                                                                                                                                                                               |
| `kit.tabs{ "A", "B", selected, on_change }`                          | Tabs                                                                                                                                                                                                                                                   |
| `kit.close{}`                                                        | A close button                                                                                                                                                                                                                                         |
| `kit.badge{ "LIVE", color, dot }`                                    | A badge                                                                                                                                                                                                                                                |
| `kit.dot{}`                                                          | A dot                                                                                                                                                                                                                                                  |
| `kit.progress{ value = 0.5 }`                                        | A progress bar                                                                                                                                                                                                                                         |
| `kit.divider{}`                                                      | A divider                                                                                                                                                                                                                                              |
| `kit.card{ image, title, text, badges, on_click }`                   | A card                                                                                                                                                                                                                                                 |
| `kit.grid{ columns = 3, gap = 6, ... }`                              | Any nodes, in rows of `columns`                                                                                                                                                                                                                        |

`kit.theme` holds the colours they use when a call names none: change it once
to restyle them all. `kit.mix(a, b, t)` mixes two `"#rrggbb"` colours.

## The rules

- A new dialog replaces the open one. Escape closes it and calls the window's
  `on_close(player)`.
- Clicks may `task.wait`. Only the pack that opened a dialog gets its clicks.
- A player who turned the resource pack down is sent no dialog: it is drawn in
  the pack's fonts. A pack-declined client answers `false` to
  `player:supports("dialog")` — and an open dialog closes from that moment.

## See also

- [Menus](/wiki/menus) — the every-client fallback for a dialog.
- [Screens and layouts](/wiki/screens) — layouts, the other pack-drawn surface.
- [UI basics](/wiki/ui-basics) — text runs and colour spellings for words in a dialog.
- [Client versions](/appendix/client-versions) — the `dialog` row and pack-declined behaviour.
