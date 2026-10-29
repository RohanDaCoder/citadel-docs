---
title: 'entitySpec.on_tick'
description: 'Runs after the physics each tick to react to where it ended up; call base(e) to extend.'
---

Part of [`entitySpec`](/ref/EntitySpec/).

```luau
entitySpec.on_tick((e: EntityHandle, base: () -> ()) -> ()) → ?
```

Runs after the physics each tick to react to where it ended up; call `base(e)` to extend.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `(e` | `EntityHandle , base: () -> ()) -> ()` | yes |

## Returns

- `?`
