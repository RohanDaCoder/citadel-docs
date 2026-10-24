---
title: "Conventions"
description: "The rules every Citadel API call follows — namespaces, vec3 positions, colours and colour names, text runs, options tables with strict field checking, the nil/false/true tri-state, and the spelling invariants."
---

:::note[In short]
the whole API follows a handful of rules. Learn them once and
every call behaves the way you expect: positions are `vec3`, colours are
`color(...)` or a name string, long calls take options tables where an
unknown field is an error, `nil`/`false` mean different things, and one
spelling serves each idea.
:::

## Namespaces

| Kind                   | Globals                                                                                                                                           |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| The main room's tables | `world`, `players`, `ui`, `game`, `rooms`, `sound` — `rooms.create{}` gives another room the same six                                             |
| Server-wide            | `fx`, `commands`, `time`, `task`, `storage`, `stores`, `http`, `network`, `shop`, `hub`, `models`, `parts`, `routes`, `data`, `fields`, `message` |
| Values and helpers     | `vec3`, `color`, `colors`, `noise`, `tween`, `camera`, `citadel`                                                                                  |

A pack is its files. `loadstring` is not there, so a pack cannot run text as
code; `require` reads only files inside the pack; `getfenv` and `setfenv` are
not there.

## Positions: `vec3`

Positions are `vec3(x, y, z)` with fields `x`, `y`, `z`. **Block positions are
floored** — `vec3(20.2, 65, -7.9)` addresses block `(20, 65, -8)` where a
block is asked for. A box's corners are `from` and `to`, in either order, both
corners inside.

## Colours

Colours are `color(r, g, b)` in `0..1`, `colors.red`, and so on, or
`color.hsv(h, s, v)` — everywhere, text included. A name string also works:

- Minecraft's sixteen: `"red"`, `"dark_aqua"`, `"light_purple"`, ...
- Six more: `"orange"`, `"lime"`, `"cyan"`, `"purple"`, `"magenta"`, `"pink"`
- `"transparent"`, or hex (`"#ff8800"`)

`colors` holds the same names. `colors.grey` is an error that lists them all —
`colors.gray` is the spelling. For more see
[Colour helpers](/ref/color/) and `color.nearest(c)`, the colour a screen or
canvas really shows, since a picture snaps to the map palette.

## Text

Text is a string, or a table of coloured runs — the full run syntax is in
[Text formatting](/ui/ui-basics/#text-runs). Every call that takes text
takes both forms.

## Options tables

Calls with more than three inputs take an options table. Every field has a
default, and **the tables are strict**:

:::caution[Gotcha]
an unknown field is an error that names the nearest valid one.
`world.display{ kind = "text", colour = "red" }` stops the script with
_no option "colour"; did you mean "color"?_ — and a field of the wrong type
is also an error.
:::

## `nil`, `false` and `true`

For optional settings that accept both, **`nil` removes an override and
`false` switches it off**. Each field documents whether it accepts `nil`:

- `player.visible = nil` shows the player again, because a player is visible
  by default. `player.visible = false` hides them.
- Where off is the default the two do the same: `display.glow = false` and
  `display.glow = nil` both remove the glow.
- A flag is `true`, `false` or `nil`. A number or a string is an error:
  `world.rules{ fall = 0 }` does not turn the rule off.

:::caution[Gotcha]
numeric settings such as `player.speed`, `player.scale` and
`player.reach` **require a number** — `nil` does not reset them.
:::

## One spelling per idea

| Idea                         | Spelling        |
| ---------------------------- | --------------- |
| A position                   | `at`            |
| Removing a thing             | `:destroy()`    |
| Stopping a timer or an event | `:cancel()`     |
| A box's corners              | `from` and `to` |

## Block names

Block names are Minecraft's, without `minecraft:`.

- Every block of every version is real here and stored exactly. An older
  client sees the nearest block its version has; a name even the newest
  version lacks becomes the nearest block. Write `"future_block|obsidian"` to
  pick the substitute yourself.
- Properties go in brackets, in any order and any subset:
  `"oak_trapdoor[facing=east]"`,
  `"stone_button[facing=west, face=wall]"`. Missing properties come from the
  default state; the nearest state wins.
- A name that is no block of any version (`"grassblock"`, `"stone_brick"`)
  is an error that lists the nearest real names.
- Queries (`game.block(name)`, the block an entity stands on) return `nil`
  for a name the game lacks.

Full treatment, including half-block `detail = 2` and player-head skins:
[Block reference](/world/block-reference/).

## Sound names

Sound names are `"<pack>.<file>"` for your assets, or vanilla names like
`"block.note_block.hat"` — see [Sound](/ui/sound/).

## Time

Time is in seconds. Only the day itself is in game units where the API says
so (see [World state](/world/world-state/)).

## What a version lacks is absent

`player.health`, `player.max_health`, `player.food` and `player.saturation`
are `nil`, not `0`, on a game version with no rule for them. Every Alpha node
is one (a0.1.0 has no food and no damage). Across the engine, **what a version
lacks is absent, not zero** — check for `nil` before you do arithmetic.

## Event subscriptions

`on_*` subscriptions return a connection; `connection:cancel()` stops the
subscription. `world.on_generate` and `world.on_populate` are single-handler
setters — see [The event model](/concepts/events/).

## See also

- [The event model](/concepts/events/) — connections, asks, deadlines.
- [Luau primer](/getting-started/luau-primer/) — the language these conventions live in.
- [Block reference](/world/block-reference/) — names, states, version fallbacks.
- [Client versions](/appendix/client-versions/) — the per-feature matrix.
