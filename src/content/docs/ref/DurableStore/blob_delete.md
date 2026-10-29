---
title: 'durableStore:blob_delete'
description: 'Deletes a player''s blob if its version is still if_version.'
---

Part of [`DurableStore`](/ref/DurableStore/).

```luau
durableStore:blob_delete(owner: string, key: string, if_version: number, lease: number ?)
```

Deletes a player's blob if its version is still `if_version`.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `owner` | `string` | yes |
| `key` | `string` | yes |
| `if_version` | `number` | yes |
| `lease` | `number` | no |
