---
title: 'citadel.budget'
description: 'This pack''s slice of a tick, and what it did with it.'
---

Part of [`citadel`](/ref/citadel/).

```luau
citadel.budget() → Budget
```

This pack's slice of a tick, and what it did with it.

## Returns

- [`Budget`](/ref/Budget/)

## Used in

> "citadel.budget()                     -- this pack's slice of a tick, and what it did with it" — [Version info](/getting-started/tooling/)
> "- `citadel.budget().asks.kinds.think` counts the bodies: `asks` sent," — [Custom entities](/entities/custom-entities/)
> "`citadel.budget().asks.kinds["entity"].missed`." — [Custom entities](/entities/custom-entities/)
> "The engine counts misses at `citadel.budget().asks.kinds["break"].missed`." — [Cancelling events](/concepts/events/)
> "Read the numbers with `citadel.budget()`:" — [Limits and reload](/systems/limits/)
> "local b = citadel.budget()" — [Limits and reload](/systems/limits/)
