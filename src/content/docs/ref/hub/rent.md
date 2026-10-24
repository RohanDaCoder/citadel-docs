---
title: "hub.rent"
description: "Offers portal slot for Gems, to lead to experience (what /play takes)"
---

Part of [`hub`](/ref/hub/).

```luau
hub.rent(player: Player | string, slot: number, product: string, experience: string ?) → string ?
```

Offers portal `slot` for Gems, to lead to `experience` (what `/play` takes). Returns the request id, or nil. More time on your own portal may leave `experience` out.

## Parameters

| Name         | Type               | Required |
| ------------ | ------------------ | -------- |
| `player`     | `Player \| string` | yes      |
| `slot`       | `number`           | yes      |
| `product`    | `string`           | yes      |
| `experience` | `string`           | no       |

## Returns

- `string ?`

## Used in

> "- `hub.rent(player, slot, product, experience)` offers a portal of the grounds for Gems, like `shop.prompt`: `product` is one of the hub's rentals, such as `portal_24h`, and `experience` the name `/play` takes of any published experience, which the portal then leads to. It returns a request id, or nil; `shop.on_paid` hands the purchase over. Renting your own portal again adds time, and may leave `experience` out to keep what it shows." — [Hub](/systems/hub/)
