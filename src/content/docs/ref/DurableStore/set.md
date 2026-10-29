---
title: 'durableStore:set'
description: 'Writes a fact if its version is still if_version, and returns the new version'
---

Part of [`DurableStore`](/ref/DurableStore/).

```luau
durableStore:set(key: string, value: any, if_version: number, lease: number ?) → number
```

Writes a fact if its version is still `if_version`, and returns the new version. A mismatch errors with {err = "conflict"}.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `key` | `string` | yes |
| `value` | `any` | yes |
| `if_version` | `number` | yes |
| `lease` | `number` | no |

## Returns

- `number`
