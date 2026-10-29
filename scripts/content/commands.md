---
title: "Commands"
url: /docs/citadel/commands
---

# Commands

```luau
commands.add(usage, function(player, args) end, opts?) -> command
--   opts = { permission = "casino.play", aliases = { "hub" }, help = "Set your bet",
--            suggest = { place = { "roulette", "arcade" }, item = function(player, typed, args) return { ... } end } }
command:suggest(arg, words)   -- a list, a function, or nil or false for nothing: what `arg` offers from now on
command:cancel()              -- takes the command away

commands.add("bet <amount:integer 1..10000> [color:red|black]", function(player, args)
    bank.bet(player, args.amount, args.color or "red")   -- args.amount is a number
end, { permission = "casino.play", help = "Bet on the wheel" })

commands.add("spawn", function(player) player:teleport(SPAWN) end, { aliases = { "hub" } })
commands.add("tekkit give <item:word> [count:integer 1..64]", give, {
    permission = "tekkit.give",
    suggest = { item = function(player, typed) return item_names() end },
})

-- A tooltip shows beside a suggestion; `args` holds what was typed before.
commands.add("pay <to:player> <amount:integer 1..>", pay, {
    suggest = { amount = function(player, typed, args)
        return { { text = tostring(bank.of(player)), tooltip = "Everything you have" }, "10", "100" }
    end },
})

-- The handle changes a list while the pack runs.
local go = commands.add("go <place:word>", go_to, { suggest = { place = { "lobby" } } })
go:suggest("place", open_places())

```
A usage is the name, any fixed words, then the arguments. `<name:type>` is
required and `[name:type]` is optional. A required argument never follows an
optional one. The types:
| type | the player types | `args.name` is |
| --- | --- | --- |
| `word` | one word | a string |
| `integer`, `integer 1..64` | a whole number, in the range if there is one | a number |
| `number`, `number 0..1` | any number, in the range if there is one | a number |
| `player` | the name of someone in this room | that player |
| `red|black` | one of the listed words | the word, in lower case |
| `text...` | the rest of the line | a string |
| `words...` | the rest of the line | a list of words |
A range may leave out either end: `integer 1..` or `integer ..64`.
`text...` and `words...` come last. An optional argument not typed is `nil`.
- **The function** may `task.wait`. A returned string shows to the player in red, such as
`return "Finish this match first"`.
- **`permission`**: without the node, a player does not see or run the
command.
- **One name, several shapes.** Calls with one name, such as `"tekkit"` and
`"tekkit give <item:word>"`, make one command. Each shape has its own
permission. The first shape the line fits runs.
- **`suggest`**, per argument: a list of words, or a function
`(player, typed, args)` that returns one. `args` holds the earlier
arguments that parse. It runs as the player types: no `task.wait`. A word may be `{ text = "arcade", tooltip = "Games" }`; 1.13+
clients show the tooltip. Only words that start with the typed text are
kept. `player` arguments and word lists (`red|black`) suggest themselves.
- **The command** handle: `command:suggest` sends the new list to every
player.
- **`help`** is the text `/help` shows after the usage. The engine’s `/help`
lists every command the player may run.
- **One pack owns a name** in a room. A second pack that adds the name or an
alias of it gets an error. `/help` and `/world` belong to the engine. A
pack command replaces a game command of the same name.
- **Per room**: `commands` is the main room’s, `room.commands` another
room’s. Destroying a room removes its commands.
