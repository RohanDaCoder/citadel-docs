---
title: "blockAmendSpec.on_use"
description: "Somebody right-clicked it; held is the item in hand"
---

Part of [`blockAmendSpec`](/ref/BlockAmendSpec/).

```luau
blockAmendSpec.on_use((block: BlockAt, player: Player ?, held: string ?, base: (... any) -> any) -> Used ?) → ?
```

Somebody right-clicked it; `held` is the item in hand. Answers "used" or "pass"; a missed deadline passes the click through.

## Parameters

| Name     | Type                                                                            | Required |
| -------- | ------------------------------------------------------------------------------- | -------- |
| `(block` | `BlockAt , player: Player ?, held: string ?, base: (... any ) -> any ) -> Used` | no       |

## Returns

- `?`
