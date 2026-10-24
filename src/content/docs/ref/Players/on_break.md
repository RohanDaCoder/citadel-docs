---
title: "players.on_break"
description: "Cancellable"
---

Part of [`players`](/ref/Players/).

```luau
players.on_break(fn: (player: Player ?, pos: Vec3, block: string) -> boolean ?) → Connection
```

Cancellable. Return `false` to stop it; return nothing to let it through. These are asked _before_ the world changes and the engine waits milliseconds for the answer, so they must be quick and must never `task.wait`. Timeout, error, overflow and disabled handlers deny the action. Across packs any `false` wins. See docs/luau-api.md, "saying no".

## Parameters

| Name | Type                                                        | Required |
| ---- | ----------------------------------------------------------- | -------- |
| `fn` | `(player: Player ?, pos: Vec3 , block: string ) -> boolean` | no       |

## Returns

- [`Connection`](/ref/Connection/)

## Used in

> "`players.on_break` and `players.on_place` run **before** the world changes. A" — [Cancelling events](/concepts/events/)
> "players.on_break(function(player, pos, block) return false end) -> connection" — [Cancelling events](/concepts/events/)
> "waits a few milliseconds for the answer. Three exist: `players.on_break`" — [Limits and reload](/systems/limits/)
