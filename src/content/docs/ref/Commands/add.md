---
title: 'commands.add'
description: 'usage: "bet <amount:integer 1..10000> [color:red|black]"'
---

Part of [`commands`](/ref/Commands/).

```luau
commands.add(usage: string, fn: (player: Player, args: { [string]: any }) -> string ?, opts: CommandOpts ?) → Command
```

usage: "bet <amount:integer 1..10000> [color:red|black]". Types: word, integer, number (with an optional min..max), player, a|b|c, text... (the rest of the line as a string), words... (as a list). args holds each argument by name; an optional one not typed is nil. Return a string and the player reads it in red.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `usage` | `string` | yes |
| `fn` | `(player: Player , args: { [ string ]: any }) -> string` | no |
| `opts` | [`CommandOpts`](/ref/CommandOpts/) | no |

## Returns

- [`Command`](/ref/Command/)

## Used in

> "commands.add("spawn", function(player)" — [Guide: Your first pack](/getting-started/quick-start/)
> "`commands.add` registers the name `"spawn"` without the slash. When a player" — [Guide: Your first pack](/getting-started/quick-start/)
> "room.commands.add("leave", function(p)" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
> "commands.add("play", function(player)" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
> "`commands.add`." — [Guide: A dungeon dimension](/guides/guide-a-dungeon-dimension/)
> "commands.add("leave", function(player)" — [Guide: A dungeon dimension](/guides/guide-a-dungeon-dimension/)
