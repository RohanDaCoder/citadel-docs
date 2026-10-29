# SOURCE: API basics

- Namespaces: `world`, `players`, `sound`, `fx`, `ui`, `commands`, `time`,
`rooms`, `storage`, `http`. Plus `task` for waiting and `require` for splitting a
pack into files.
- A pack is its files. `loadstring` is not there, so a pack cannot run text
as code, and `require` reads only files inside the pack. `getfenv` and
`setfenv` are not there.
- The first six belong to the main room. `rooms.create{}` gives another room
the same six tables.
- Event subscriptions are `on_*` and return a connection;
`connection:cancel()` stops the subscription. `world.on_generate` and
`world.on_populate` are single-handler setters: a later call replaces the
previous handler, and they return nothing.
- Positions are `vec3(x, y, z)` with fields `x y z`. Block positions are
floored.
- Colours are `color(r, g, b)` in `0..1`, `colors.red`, …, or
`color.hsv(h, s, v)`, everywhere, text included.
  - A name string also works: Minecraft’s
sixteen (`"red"`, `"dark_aqua"`, `"light_purple"`, …), six more
(`"orange"`, `"lime"`, `"cyan"`, `"purple"`, `"magenta"`, `"pink"`),
`"transparent"`, or hex (`"#ff8800"`).
  - `colors` holds the same names. `colors.grey` is an error that lists
them.
- Text is a string or a table of coloured runs. See “Text formatting”.
- Calls with more than three inputs take an options table. Every field has
a default.
  - **An unknown field is an error** that names the nearest valid one:
`world.display{ kind = "text", colour = "red" }` stops the script with
*no option “colour”; did you mean “color”?*
  - A field of the wrong type is also an error.
- For optional settings that accept both, `nil` removes an override and
`false` switches it off. Each field documents whether it accepts `nil`.
Numeric settings such as `player.speed`, `player.scale` and `player.reach`
require a number; `nil` does not reset them.
  - `player.visible = nil` shows the player again, because a player is
visible by default.
  - Where off is the default, the two do the same: `display.glow = false`
and `display.glow = nil` both remove the glow.
  - A flag is `true`, `false` or `nil`. A number or a string is an error:
`world.rules{ fall = 0 }` does not turn the rule off.
- One spelling per idea: a position is `at`, removing a thing is
`:destroy()`, stopping a timer or an event is `:cancel()`, and a box’s
corners are `from` and `to`.
- Block names are Minecraft’s, without `minecraft:`.
  - Every block of every version is real here and stored exactly. An older
client sees the nearest block its version has.
  - A name even the newest version lacks becomes the nearest block. Write
`"future_block|obsidian"` to pick the substitute yourself.
  - Properties go in brackets, in any order and any subset:
`"oak_trapdoor[facing=east]"`, `"stone_button[facing=west, face=wall]"`.
Missing properties come from the default state. The nearest state wins.
  - A name that is no block of any version (`"grassblock"`,
`"stone_brick"`) is an error that lists the nearest real names.
  - Queries (`game.block(name)`, the block an entity stands on) return `nil` for
a name the game lacks.
- Sound names are `"<pack>.<file>"` for your assets, or vanilla names like
`"block.note_block.hat"`.
- Time is in seconds. Only the day is in ticks (24000 to a day).
- Nothing is global state except the callbacks you register.
