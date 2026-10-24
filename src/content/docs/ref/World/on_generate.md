---
title: "world.on_generate"
description: "Called for a chunk each time it comes into memory, in a script world; it must make the same blocks every time."
---

Part of [`world`](/ref/World/).

```luau
world.on_generate(fn: (chunk: Chunk) -> ())
```

Called for a chunk each time it comes into memory, in a script world; it must make the same blocks every time.

## Parameters

| Name | Type                    | Required |
| ---- | ----------------------- | -------- |
| `fn` | `(chunk: Chunk ) -> ()` | yes      |

## Used in

> "world.on_generate(function(chunk)" — [Guide: Your first pack](/getting-started/quick-start/)
> "blocks deep. `world.on_generate` registers a function that Citadel calls" — [Guide: Your first pack](/getting-started/quick-start/)
> "world.on_generate(function(chunk)" — [Guide: Coin rush](/guides/guide-coin-rush/)
> "world.on_generate(function(chunk)" — [Guide: Coin rush](/guides/guide-coin-rush/)
> "world.on_generate(function(chunk)" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
> "A room's `generate` works like `world.on_generate`: it must make the same" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
