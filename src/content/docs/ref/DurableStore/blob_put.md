---
title: 'durableStore:blob_put'
description: 'Writes a player''s binary blob if its version is still if_version, and returns the new version'
---

Part of [`DurableStore`](/ref/DurableStore/).

```luau
durableStore:blob_put(owner: string, key: string, bytes: string, if_version: number, lease: number ?) → number
```

Writes a player's binary blob if its version is still `if_version`, and returns the new version. At most 32 MiB.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `owner` | `string` | yes |
| `key` | `string` | yes |
| `bytes` | `string` | yes |
| `if_version` | `number` | yes |
| `lease` | `number` | no |

## Returns

- `number`
