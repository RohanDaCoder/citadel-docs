---
title: "asks.kinds"
url: /docs/citadel/reference/Asks/kinds
---

# asks.kinds

The same counters per kind of question, e.g. `kinds["break"].missed`.

```
asks.kinds: { [string]: AskCount }
```


## Used in
- [`- `citadel.budget().asks.kinds.think` counts the bodies: `asks` sent,`Custom entities](/docs/citadel/custom-entities)
- [``citadel.budget().asks.kinds["entity"].missed`.`Custom entities](/docs/citadel/custom-entities)
- [`The engine counts misses at `citadel.budget().asks.kinds["break"].missed`.`Cancelling events](/docs/citadel/cancelling-events)
- [`for kind, count in citadel.budget().asks.kinds do`Limits and reload](/docs/citadel/limits-and-reload)
