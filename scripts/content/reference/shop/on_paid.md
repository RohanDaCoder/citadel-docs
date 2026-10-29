---
title: "shop.on_paid"
url: /docs/citadel/reference/shop/on_paid
---

# shop.on_paid

Called once per paid purchase; returning without an error hands it over. An error leaves it waiting, to be called again later.

```
shop.on_paid(handler: (purchase: ShopPurchase) -> ()) → Connection
```


## Parameters


## Returns


## Used in
- [`shop.on_paid(function(purchase)`Shop](/docs/citadel/shop)
- [`- `shop.on_paid(fn)` calls `fn({request, player, product})` for each undelivered paid purchase. It runs on the server the player is on: an experience has many servers, and each one hands over only to its own players. A purchase for a player who is not online waits until they join one. At least one active paid handler must complete successfully, and all active paid handlers must succeed, before the purchase is acknowledged. With no paid handler, or if one raises an error, it stays pending. An `on_declined` listener alone never acknowledges a paid purchase. Delivery can repeat after a failure or restart; use `purchase.request` as a durable idempotency key when granting a reward.`Shop](/docs/citadel/shop)
- [`- `hub.rent(player, slot, product, experience)` offers a portal of the grounds for Gems, like `shop.prompt`: `product` is one of the hub's rentals, such as `portal_24h`, and `experience` the name `/play` takes of any published experience, which the portal then leads to. It returns a request id, or nil; `shop.on_paid` hands the purchase over. Renting your own portal again adds time, and may leave `experience` out to keep what it shows.`Hub](/docs/citadel/hub)
