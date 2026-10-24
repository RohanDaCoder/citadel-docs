---
title: "durableStore:delete"
description: "Removes a fact if its version is still if_version."
---

Part of [`DurableStore`](/ref/DurableStore/).

```luau
durableStore:delete(key: string, if_version: number, lease: number ?)
```

Removes a fact if its version is still `if_version`.

## Parameters

| Name         | Type     | Required |
| ------------ | -------- | -------- |
| `key`        | `string` | yes      |
| `if_version` | `number` | yes      |
| `lease`      | `number` | no       |
