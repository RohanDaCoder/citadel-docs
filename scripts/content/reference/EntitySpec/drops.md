---
title: "entitySpec.drops"
url: /docs/citadel/reference/EntitySpec/drops
---

# entitySpec.drops

physics = "living" only: what it leaves when it dies. Each row is { item = "stick", count = 2 }, count = { least, most } for a random count, chance = 0.05 for a row that comes from one death in twenty, or a pack item. false or nil: nothing.

```
entitySpec.drops: ({ { [string]: any } } | false)?
```
