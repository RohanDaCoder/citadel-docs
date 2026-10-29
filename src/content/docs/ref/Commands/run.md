---
title: 'commands.run'
description: 'Runs a pack''s command for player as if they typed it ("/servers"), with their permissions'
---

Part of [`commands`](/ref/Commands/).

```luau
commands.run(player: Player, line: string) → boolean
```

Runs a pack's command for player as if they typed it ("/servers"), with their permissions. false when no pack in their room declared it.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `player` | [`Player`](/ref/Player/) | yes |
| `line` | `string` | yes |

## Returns

- `boolean`

## Used in

> "commands.run(player, line) -> boolean   -- runs a pack's command for player, as if they typed it" — [Commands](/systems/commands/)
> "- **`commands.run`** runs a line for a player as if they typed it, so one" — [Commands](/systems/commands/)
