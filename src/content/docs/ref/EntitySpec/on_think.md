---
title: "entitySpec.on_think"
description: "define only"
---

Part of [`entitySpec`](/ref/EntitySpec/).

```luau
entitySpec.on_think((b: Think) -> ()) → ?
```

define only. The brain: one call for all due bodies of the kind, with their numbers in columns. The engine never waits for it; the answer lands on the next tick it is there, and is never dropped.

## Parameters

| Name | Type            | Required |
| ---- | --------------- | -------- |
| `(b` | `Think ) -> ()` | yes      |

## Returns

- `?`
