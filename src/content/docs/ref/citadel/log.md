---
title: "citadel.log"
description: "Writes its arguments to the server log, under this pack's name."
---

Part of [`citadel`](/ref/citadel/).

```luau
citadel.log(... any)
```

Writes its arguments to the server log, under this pack's name.

## Parameters

| Name     | Type  | Required |
| -------- | ----- | -------- |
| `...any` | `any` | yes      |

## Used in

> "citadel.log("anything", 42) -- to the server log, under this pack's name" — [Version info](/getting-started/tooling/)
> "citadel.log(`slow at {kind}: {count.missed} of {count.asks} missed`)" — [Limits and reload](/systems/limits/)
