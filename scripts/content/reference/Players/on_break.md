---
title: "players.on_break"
url: /docs/citadel/reference/Players/on_break
---

# players.on_break

Cancellable. Return `false` to stop it; return nothing to let it through. These are asked *before* the world changes and the engine waits milliseconds for the answer, so they must be quick and must never `task.wait`. Timeout, error, overflow and disabled handlers deny the action. Across packs any `false` wins. See docs/luau-api.md, "saying no".

```
players.on_break(fn: (player: Player?, pos: Vec3, block: string) -> boolean?) → Connection
```


## Parameters


## Returns


## Used in
- [``players.on_break` and `players.on_place` run **before** the world changes. A`Cancelling events](/docs/citadel/cancelling-events)
- [`players.on_break(function(player, pos, block) return false end) -> connection`Cancelling events](/docs/citadel/cancelling-events)
- [`waits a few milliseconds for the answer. Three exist: `players.on_break``Limits and reload](/docs/citadel/limits-and-reload)
