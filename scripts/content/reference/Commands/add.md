---
title: "commands.add"
url: /docs/citadel/reference/Commands/add
---

# commands.add

usage: "bet <amount:integer 1..10000> [color:red|black]". Types: word, integer, number (with an optional min..max), player, a|b|c, text... (the rest of the line as a string), words... (as a list). args holds each argument by name; an optional one not typed is nil. Return a string and the player reads it in red.

```
commands.add(usage: string, fn: (player: Player, args: { [string]: any }) -> string?, opts: CommandOpts?) → Command
```


## Parameters


## Returns


## Used in
- [`commands.add("spawn", function(player)`Guide: Your first pack](/docs/citadel/guides/your-first-pack)
- [``commands.add` registers the name `"spawn"` without the slash. When a player`Guide: Your first pack](/docs/citadel/guides/your-first-pack)
- [`room.commands.add("leave", function(p)`Guide: Parkour, a room each](/docs/citadel/guides/parkour-a-room-each)
- [`commands.add("play", function(player)`Guide: Parkour, a room each](/docs/citadel/guides/parkour-a-room-each)
- [``commands.add`.`Guide: A dungeon dimension](/docs/citadel/guides/a-dungeon-dimension)
- [`commands.add("leave", function(player)`Guide: A dungeon dimension](/docs/citadel/guides/a-dungeon-dimension)
- [`commands.add("spawn", function(player)`Your first pack](/docs/citadel/your-first-pack)
- [`- `commands.add` registers `spawn` without a slash. When a player types`Your first pack](/docs/citadel/your-first-pack)
