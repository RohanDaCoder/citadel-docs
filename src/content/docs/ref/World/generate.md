---
title: 'world.generate'
description: 'Declares this world: the engine makes each chunk from the rules, on every core, and no script runs for a chunk.'
---

Part of [`world`](/ref/World/).

```luau
world.generate(rules: GeneratorRules) → Generated
```

Declares this world: the engine makes each chunk from the rules, on every core, and no script runs for a chunk.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `rules` | [`GeneratorRules`](/ref/GeneratorRules/) | yes |

## Returns

- [`Generated`](/ref/Generated/)

## Used in

> "`world.generate` declares a world as rules. The engine makes each chunk from" — [Blocks and terrain](/world/terrain-generation/)
> "local made = world.generate {" — [Blocks and terrain](/world/terrain-generation/)
