---
title: "blockSpec.on_random_tick"
description: "The random pass landed on it"
---

Part of [`blockSpec`](/ref/BlockSpec/).

```luau
blockSpec.on_random_tick((block: BlockAt, base: (... any) -> any) -> ()) → ?
```

The random pass landed on it. Not the same thing as `on_tick`, which is why it has the longer name.

## Parameters

| Name     | Type                                        | Required |
| -------- | ------------------------------------------- | -------- |
| `(block` | `BlockAt , base: (... any ) -> any ) -> ()` | yes      |

## Returns

- `?`
