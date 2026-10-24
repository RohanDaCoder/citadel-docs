---
title: "blockSpec.on_use"
description: "The hooks"
---

Part of [`blockSpec`](/ref/BlockSpec/).

```luau
blockSpec.on_use((block: BlockAt, player: Player ?, held: string ?, base: (... any) -> any) -> Used ?) → ?
```

The hooks. Writing one is what asks for it — there is no flag beside `on_random_tick` saying the random pass may land here.

## Parameters

| Name     | Type                                                                            | Required |
| -------- | ------------------------------------------------------------------------------- | -------- |
| `(block` | `BlockAt , player: Player ?, held: string ?, base: (... any ) -> any ) -> Used` | no       |

## Returns

- `?`
