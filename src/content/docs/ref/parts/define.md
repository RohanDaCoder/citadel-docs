---
title: "parts.define"
description: "Declares a named part and its generator; nothing runs on load"
---

Part of [`parts`](/ref/parts/).

```luau
parts.define(def: PartDefinition)
```

Declares a named part and its generator; nothing runs on load. A generator runs on request, or when its code changes.

## Parameters

| Name  | Type                                     | Required |
| ----- | ---------------------------------------- | -------- |
| `def` | [`PartDefinition`](/ref/PartDefinition/) | yes      |

## Used in

> "`parts.define` declares a named part whose generator runs on request." — [Server settings](/systems/server-settings/)
> "\| `PART_OVERLAP` \| advice \| two parts (`parts.define`) overlap without one inside the other: regenerating either rewrites the other \|" — [Blocks and terrain](/world/terrain-generation/)
> "parts.define {" — [Named parts](/world/building/)
> "- **Nothing runs on load.** `parts.define` only declares the part. A" — [Named parts](/world/building/)
