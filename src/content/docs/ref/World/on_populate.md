---
title: "world.on_populate"
description: "Each chunk the overworld terrain made, once, after it made it."
---

Part of [`world`](/ref/World/).

```luau
world.on_populate(fn: (chunk: Chunk) -> ())
```

Each chunk the overworld terrain made, once, after it made it.

## Parameters

| Name | Type                    | Required |
| ---- | ----------------------- | -------- |
| `fn` | `(chunk: Chunk ) -> ()` | yes      |

## Used in

> "trees and sea level 63. Scripts only add to it (`world.on_populate`)." — [Server settings](/systems/server-settings/)
> "`world.on_populate` are single-handler setters: a later call replaces the" — [API basics](/concepts/conventions/)
> "world.on_populate(function(chunk) end) -- add to the overworld's own chunks; see "populating the overworld"" — [Blocks and terrain](/world/terrain-generation/)
> "world.on_populate(function(chunk) end) -- once per chunk the overworld terrain made, after it made it" — [Blocks and terrain](/world/terrain-generation/)
