---
title: "blockAmendSpec.on_power"
description: "A redstone signal started (powered is true) or stopped reaching it"
---

Part of [`blockAmendSpec`](/ref/BlockAmendSpec/).

```luau
blockAmendSpec.on_power((block: BlockAt, powered: boolean, base: (... any) -> any) -> ()) → ?
```

A redstone signal started (`powered` is true) or stopped reaching it. Called once for each, not for every change beside it.

## Parameters

| Name     | Type                                                           | Required |
| -------- | -------------------------------------------------------------- | -------- |
| `(block` | `BlockAt , powered: boolean , base: (... any ) -> any ) -> ()` | yes      |

## Returns

- `?`
