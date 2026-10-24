---
title: "entitySpec.on_steer"
description: "Runs before the physics each tick to decide where it goes; call base(e) to extend, leave it out to replace."
---

Part of [`entitySpec`](/ref/EntitySpec/).

```luau
entitySpec.on_steer((e: EntityHandle, base: () -> ()) -> ()) → ?
```

Runs before the physics each tick to decide where it goes; call `base(e)` to extend, leave it out to replace.

## Parameters

| Name | Type                                   | Required |
| ---- | -------------------------------------- | -------- |
| `(e` | `EntityHandle , base: () -> ()) -> ()` | yes      |

## Returns

- `?`
