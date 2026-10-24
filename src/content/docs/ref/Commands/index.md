---
title: "commands global · type Commands"
description: "Adds a room's slash commands from a usage line: the commands global, or room.commands."
---

Adds a room's slash commands from a usage line: the `commands` global, or `room.commands`.

Part of the [Player lifecycle](/players/player-lifecycle/) article.

## Functions

| Call                        | Purpose                                                                                                                                                                                                                                                                                                                     |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`add`](/ref/Commands/add/) | usage: "bet <amount:integer 1..10000> [color:red\|black]". Types: word, integer, number (with an optional min..max), player, a\|b\|c, text... (the rest of the line as a string), words... (as a list). args holds each argument by name; an optional one not typed is nil. Return a string and the player reads it in red. |
