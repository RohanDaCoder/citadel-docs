---
title: "blockSpec.on_place"
description: "A player put it down; block.data is empty then, ready to be filled."
---

Part of [`blockSpec`](/ref/BlockSpec/).

```luau
blockSpec.on_place((block: BlockAt, player: Player ?, base: (... any) -> any) -> ()) → ?
```

A player put it down; `block.data` is empty then, ready to be filled.

## Parameters

| Name     | Type                                                          | Required |
| -------- | ------------------------------------------------------------- | -------- |
| `(block` | `BlockAt , player: Player ?, base: (... any ) -> any ) -> ()` | yes      |

## Returns

- `?`
