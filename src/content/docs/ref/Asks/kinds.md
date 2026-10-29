---
title: 'asks.kinds'
description: 'The same counters per kind of question, e.g'
---

Part of [`asks`](/ref/Asks/).

```luau
asks.kinds: { [string]: AskCount }
```

The same counters per kind of question, e.g. `kinds["break"].missed`.

## Used in

> "- `citadel.budget().asks.kinds.think` counts the bodies: `asks` sent," — [Custom entities](/entities/custom-entities/)
> "`citadel.budget().asks.kinds["entity"].missed`." — [Custom entities](/entities/custom-entities/)
> "The engine counts misses at `citadel.budget().asks.kinds["break"].missed`." — [Cancelling events](/concepts/events/)
> "for kind, count in citadel.budget().asks.kinds do" — [Limits and reload](/systems/limits/)
