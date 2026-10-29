---
title: 'shop.prompt'
description: 'Asks Minefort to offer product to the player'
---

Part of [`shop`](/ref/shop/).

```luau
shop.prompt(player: Player | string, product: string) → string ?
```

Asks Minefort to offer `product` to the player. Returns the request id, or nil when it was not offered.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `player` | `Player \| string` | yes |
| `product` | `string` | yes |

## Returns

- `string ?`

## Used in

> "shop.prompt(player, "vip") -- Minefort shows its dialog" — [Shop](/systems/shop/)
> "- `shop.prompt(player, product)` returns a request id, or nil when Minefort did not offer it. A player or a uuid string." — [Shop](/systems/shop/)
> "- `hub.rent(player, slot, product, experience)` offers a portal of the grounds for Gems, like `shop.prompt`: `product` is one of the hub's rentals, such as `portal_24h`, and `experience` the name `/play` takes of any published experience, which the portal then leads to. It returns a request id, or nil; `shop.on_paid` hands the purchase over. Renting your own portal again adds time, and may leave `experience` out to keep what it shows." — [Hub](/systems/hub/)
