---
title: "hub.rent"
url: /docs/citadel/reference/hub/rent
---

# hub.rent

Offers portal `slot` for Gems, to lead to `experience` (what `/play` takes). Returns the request id, or nil. More time on your own portal may leave `experience` out.

```
hub.rent(player: Player | string, slot: number, product: string, experience: string?) → string?
```


## Parameters


## Returns


## Used in
- [`- `hub.rent(player, slot, product, experience)` offers a portal of the grounds for Gems, like `shop.prompt`: `product` is one of the hub's rentals, such as `portal_24h`, and `experience` the name `/play` takes of any published experience, which the portal then leads to. It returns a request id, or nil; `shop.on_paid` hands the purchase over. Renting your own portal again adds time, and may leave `experience` out to keep what it shows.`Hub](/docs/citadel/hub)
