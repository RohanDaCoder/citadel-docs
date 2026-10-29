---
title: 'citadel.on_slow'
description: 'Called when a batch runs out of budget; at most once a second.'
---

Part of [`citadel`](/ref/citadel/).

```luau
citadel.on_slow(fn: (slow: Slow) -> ()) → Connection
```

Called when a batch runs out of budget; at most once a second.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `fn` | `(slow: Slow ) -> ()` | yes |

## Returns

- [`Connection`](/ref/Connection/)

## Used in

> "citadel.on_slow(function(slow) end)  -- a batch that ran out of budget; see "Limits and reload"" — [Version info](/getting-started/tooling/)
> "citadel.on_slow(function(slow)" — [Limits and reload](/systems/limits/)
