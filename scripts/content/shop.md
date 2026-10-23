---
title: "Shop"
url: /docs/citadel/shop
---

# Shop

**The player says yes or no in Minefort’s own dialog, not in the pack.** The pack learns only whether a purchase was paid. It never sees the player’s Gems, the price or a reason.
```luau
players.on_join(function(player)
    if shop.owns(player, "vip") then
        player:message("Welcome back, VIP")
    else
        shop.prompt(player, "vip") -- Minefort shows its dialog
    end
end)

shop.on_paid(function(purchase)
    -- Hand the item over here. Returning without an error marks it delivered.
    for _, player in players.list() do
        if player.uuid == purchase.player then player:message("Thanks for buying VIP") end
    end
end)

shop.on_declined(function(purchase)
    -- The player said no, or did not answer. Close the pack's own shop screen.
end)

```
- `shop.prompt(player, product)` returns a request id, or nil when Minefort did not offer it. A player or a uuid string.
- `shop.owns(player, product)` returns whether the player owns a pass.
- `shop.on_paid(fn)` calls `fn({request, player, product})` for each undelivered paid purchase. It runs on the server the player is on: an experience has many servers, and each one hands over only to its own players. A purchase for a player who is not online waits until they join one. At least one active paid handler must complete successfully, and all active paid handlers must succeed, before the purchase is acknowledged. With no paid handler, or if one raises an error, it stays pending. An `on_declined` listener alone never acknowledges a paid purchase. Delivery can repeat after a failure or restart; use `purchase.request` as a durable idempotency key when granting a reward.
- `shop.on_declined(fn)` calls `fn({request, player, product})` when the player said no or did not answer.
- A product key is 1 to 32 characters of `a-z`, `0-9`, `_` and `-`. Another key is an error.
Calls yield, like `stores`. Only experiences in the Minefort Creator Rewards Program have the shop. Elsewhere, and in local runs, `prompt` returns nil and `owns` returns false.
After an error, read again. After an I/O timeout, a write may have committed. Retry only versioned writes, never an increment. A world release rollback does not rewind shared facts or blobs.
