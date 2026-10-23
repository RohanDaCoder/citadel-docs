---
title: "shop.prompt"
url: /docs/citadel/reference/shop/prompt
---

# shop.prompt

Asks Minefort to offer `product` to the player. Returns the request id, or nil when it was not offered.

```
shop.prompt(player: Player | string, product: string) → string?
```


## Parameters


## Returns


## Used in
- [`shop.prompt(player, "vip") -- Minefort shows its dialog`Shop](/docs/citadel/shop)
- [`- `shop.prompt(player, product)` returns a request id, or nil when Minefort did not offer it. A player or a uuid string.`Shop](/docs/citadel/shop)
- [`- `hub.rent(player, slot, product, experience)` offers a portal of the grounds for Gems, like `shop.prompt`: `product` is one of the hub's rentals, such as `portal_24h`, and `experience` the name `/play` takes of any published experience, which the portal then leads to. It returns a request id, or nil; `shop.on_paid` hands the purchase over. Renting your own portal again adds time, and may leave `experience` out to keep what it shows.`Hub](/docs/citadel/hub)
