---
title: "shop.owns"
description: "Whether the player owns this pass."
---

Part of [`shop`](/ref/shop/).

```luau
shop.owns(player: Player | string, product: string) → boolean
```

Whether the player owns this pass.

## Parameters

| Name      | Type               | Required |
| --------- | ------------------ | -------- |
| `player`  | `Player \| string` | yes      |
| `product` | `string`           | yes      |

## Returns

- `boolean`

## Used in

> "if shop.owns(player, "vip") then" — [Shop](/systems/shop/)
> "- `shop.owns(player, product)` returns whether the player owns a pass." — [Shop](/systems/shop/)
