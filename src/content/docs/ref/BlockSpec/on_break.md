---
title: "blockSpec.on_break"
description: "Something broke it"
---

Part of [`blockSpec`](/ref/BlockSpec/).

```luau
blockSpec.on_break((block: BlockAt, player: Player ?, by: Breaker, base: (... any) -> any) -> Drops ?) → ?
```

Something broke it. Answers "none", "table" or a drops list; fails closed to the definition's `drops`.

## Parameters

| Name     | Type                                                                           | Required |
| -------- | ------------------------------------------------------------------------------ | -------- |
| `(block` | `BlockAt , player: Player ?, by: Breaker , base: (... any ) -> any ) -> Drops` | no       |

## Returns

- `?`
