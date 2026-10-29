---
title: Commands
section: systems
order: 1
description: commands.add builds slash commands from a usage line — the argument types and ranges, permission nodes, aliases, tab-completion suggestions with tooltips, one name with several shapes; and commands.run fires a pack's command for a player as if they typed it.
tags: [commands, usage line, suggestions, permissions, aliases, help]
---
# Commands

> **In short:** a pack adds slash commands with `commands.add` from a usage
> string that doubles as the grammar: `<name:type>` marks a required argument,
> `[name:type]` an optional one. This page covers the usage grammar, the
> argument types and what `args.name` becomes, the `opts` table (permission,
> aliases, help, suggest), tab-completion with tooltips, several shapes under
> one name, and the rules of who owns a command name in a room.

## Adding a command

```luau
commands.add(usage, function(player, args) end, opts?) -> command
--   opts = { permission = "casino.play", aliases = { "hub" }, help = "Set your bet",
--            suggest = { place = { "roulette", "arcade" }, item = function(player, typed, args) return { ... } end } }
command:suggest(arg, words)   -- a list, a function, or nil or false for nothing: what `arg` offers from now on
command:cancel()              -- takes the command away
```

`commands.add` takes the usage line, the function that runs it, and options;
it returns a [`Command`](/ref/Command) handle. The function receives the
player who typed it and a table holding each argument by name — an optional
argument that was not typed is `nil`.

```luau
commands.add("bet <amount:integer 1..10000> [color:red|black]", function(player, args)
    bank.bet(player, args.amount, args.color or "red")   -- args.amount is a number
end, { permission = "casino.play", help = "Bet on the wheel" })

commands.add("spawn", function(player) player:teleport(SPAWN) end, { aliases = { "hub" } })
commands.add("tekkit give <item:word> [count:integer 1..64]", give, {
    permission = "tekkit.give",
    suggest = { item = function(player, typed) return item_names() end },
})
```

## The usage line

A usage is the name, any fixed words, then the arguments. Fixed words let one
name carry several shapes — see [One name, several shapes](#one-name-several-shapes).

- `<name:type>` is required and `[name:type]` is optional.
- **A required argument never follows an optional one.**
- A range may leave out either end: `integer 1..` or `integer ..64`.
- `text...` and `words...` come last.

## Argument types

What the player types, and what `args.name` is inside the function:

| type | the player types | `args.name` is |
| --- | --- | --- |
| `word` | one word | a string |
| `integer`, `integer 1..64` | a whole number, in the range if there is one | a number |
| `number`, `number 0..1` | any number, in the range if there is one | a number |
| `player` | the name of someone in this room | that player |
| `red|black` | one of the listed words | the word, in lower case |
| `text...` | the rest of the line | a string |
| `words...` | the rest of the line | a list of words |

## The function and what it returns

The function runs when a player types the command and the line fits. Two
behaviour rules:

- **The function may `task.wait`.** A command is an input event, outside the
  tick budget but under the 100 ms runaway limit (see
  [Limits](/wiki/limits)).
- **A returned string shows to the player in red**, such as
  `return "Finish this match first"`. It is the built-in way to refuse.

## Options

| Option | Type | Meaning |
| --- | --- | --- |
| `permission` | string | A permission node; without it, a player does not see or run the command. |
| `aliases` | `{ string }` | More names for the same command, such as `{ "hub" }`. |
| `help` | string | The text `/help` shows after the usage. |
| `suggest` | `{ [arg]: list or function }` | Per argument: the words to offer as the player types. |

`/help` is the engine's own: it lists **every command the player may run**, so
a command behind a permission node the player lacks does not appear there.

## Suggestions

`suggest` is per argument name: a list of words, or a function
`(player, typed, args)` that returns one. `args` holds the earlier arguments
that parse. It runs as the player types: **no `task.wait`**.

```luau
-- A tooltip shows beside a suggestion; `args` holds what was typed before.
commands.add("pay <to:player> <amount:integer 1..>", pay, {
    suggest = { amount = function(player, typed, args)
        return { { text = tostring(bank.of(player)), tooltip = "Everything you have" }, "10", "100" }
    end },
})
```

- A word may be `{ text = "arcade", tooltip = "Games" }`; **1.13+ clients show
  the tooltip**.
- Only words that start with the typed text are kept.
- `player` arguments and word lists (`red|black`) suggest themselves.

The handle changes a list while the pack runs — `command:suggest` sends the
new list to every player:

```luau
-- The handle changes a list while the pack runs.
local go = commands.add("go <place:word>", go_to, { suggest = { place = { "lobby" } } })
go:suggest("place", open_places())
```

Pass `nil` or `false` to offer nothing from now on. `command:cancel()` takes
the command away entirely.

## One name, several shapes

Calls with one name, such as `"tekkit"` and
`"tekkit give <item:word>"`, make one command. Each shape has its own
permission. **The first shape the line fits runs.**

## Who owns a name

- **One pack owns a name** in a room. A second pack that adds the name or an
  alias of it gets an error.
- `/help` and `/world` belong to the engine.
- A pack command replaces a game command of the same name.

> **Gotcha:** aliases claim the name too — adding `/spawn` with the alias
> `"hub"` blocks every other pack in the room from either name.

## Per room

- [`commands.run(player, line)`](/ref/Commands/run) runs a line for a player
  as if they typed it, so one pack opens what another declared: a compass
  runs `"/servers"`, whichever pack owns it. The player's own permissions
  apply. Only a command a pack declared in the player's room runs; `false`
  means none did, and the engine's and the game's commands are never run
  this way.

`commands` is the main room's, `room.commands` another room's. Destroying a
room removes its commands (see
[Rooms and dimensions](/wiki/rooms-and-dimensions)).

## See also

- [Permissions](/wiki/permissions) — the permission nodes `opts.permission` checks.
- [The event model](/wiki/events) — commands as input events, and what may `task.wait`.
- [Limits](/wiki/limits) — the 100 ms runaway limit that covers commands.
- [`commands.add`](/ref/Commands/add) — the reference entry.
- [`Command`](/ref/Command) — the handle: `:suggest` and `:cancel`.
