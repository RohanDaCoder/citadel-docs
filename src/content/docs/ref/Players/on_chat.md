---
title: 'players.on_chat'
description: 'Return false and the line is not said.'
---

Part of [`players`](/ref/Players/).

```luau
players.on_chat(fn: (player: Player, text: string) -> boolean ?) → Connection
```

Return false and the line is not said.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `fn` | `(player: Player , text: string ) -> boolean` | no |

## Returns

- [`Connection`](/ref/Connection/)

## Used in

> "players.on_chat(function(player, text) end) -> connection     -- return false and the line is not said" — [Input](/players/movement/)
> "The first `players.on_chat` takes over chat in its room. Each line is then" — [Input](/players/movement/)
