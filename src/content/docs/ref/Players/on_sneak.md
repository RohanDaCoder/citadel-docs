---
title: "players.on_sneak"
description: "Calls fn once per sneak press and release; down is true on the press."
---

Part of [`players`](/ref/Players/).

```luau
players.on_sneak(fn: (player: Player, down: boolean) -> ()) → Connection
```

Calls `fn` once per sneak press and release; `down` is true on the press.

## Parameters

| Name | Type                                      | Required |
| ---- | ----------------------------------------- | -------- |
| `fn` | `(player: Player , down: boolean ) -> ()` | yes      |

## Returns

- [`Connection`](/ref/Connection/)

## Used in

> "players.on_sneak(function(player, down) end) -> connection -- once per press and release" — [Input](/players/movement/)
> "- Without `locked`, sneaking gets a rider off and fires `players.on_sneak`." — [Displays](/ui/displays/)
