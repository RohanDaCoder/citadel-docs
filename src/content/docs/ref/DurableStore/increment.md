---
title: 'durableStore:increment'
description: 'Adds by to a number atomically, starting at zero, and returns the result'
---

Part of [`DurableStore`](/ref/DurableStore/).

```luau
durableStore:increment(key: string, by: number) → number
```

Adds `by` to a number atomically, starting at zero, and returns the result. Never retry it blindly after a timeout.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `key` | `string` | yes |
| `by` | `number` | yes |

## Returns

- `number`
