---
title: 'entitySpec.on_remove'
description: 'Told when it goes; why is "removed", "settled", "killed" or "unloaded"'
---

Part of [`entitySpec`](/ref/EntitySpec/).

```luau
entitySpec.on_remove((e: EntityHandle, why: string ?) -> ()) → ?
```

Told when it goes; `why` is "removed", "settled", "killed" or "unloaded". Not called when the pack goes away.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `(e` | `EntityHandle , why: string ?) -> ()` | yes |

## Returns

- `?`
