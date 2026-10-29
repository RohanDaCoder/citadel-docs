---
title: 'entityAmendSpec.on_remove'
description: 'Called when it leaves the world; why is "removed", "settled", "killed" or "unloaded"'
---

Part of [`entityAmendSpec`](/ref/EntityAmendSpec/).

```luau
entityAmendSpec.on_remove((e: EntityHandle, why: string ?) -> ()) → ?
```

Called when it leaves the world; `why` is "removed", "settled", "killed" or "unloaded". Not called when the pack goes away.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `(e` | `EntityHandle , why: string ?) -> ()` | yes |

## Returns

- `?`
