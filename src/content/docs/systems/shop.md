---
title: "Shop"
description: "Selling products for Gems — shop.prompt and shop.owns, the on_paid delivery contract with its all-handlers-must-succeed acknowledgement, on_declined, product keys, and the retry and idempotence rules."
---

:::note[In short]
`shop` sells an experience's products for Minefort Gems. The
player says yes or no in **Minefort's own dialog** — the pack learns only
whether a purchase was paid, never the balance, the price or a reason.
This page covers prompting, checking ownership, the `on_paid` delivery
contract and its acknowledgement rules, `on_declined`, and the retry rules
that make delivery exactly once.
:::

## The privacy model

**The player says yes or no in Minefort's own dialog, not in the pack.** The
pack learns only whether a purchase was paid. It never sees the player's
Gems, the price or a reason. A pack's own shop screen can offer and explain,
but the transaction itself is Minefort's.

## Prompting and checking ownership

```luau
players.on_join(function(player)
    if shop.owns(player, "vip") then
        player:message("Welcome back, VIP")
    else
        shop.prompt(player, "vip") -- Minefort shows its dialog
    end
end)
```

| Call                           | Returns            | Purpose                                                  |
| ------------------------------ | ------------------ | -------------------------------------------------------- |
| `shop.prompt(player, product)` | request id, or nil | Minefort shows its dialog; nil when it did not offer it. |
| `shop.owns(player, product)`   | boolean            | Whether the player owns a pass.                          |
| `shop.on_paid(fn)`             | Connection         | Called for each undelivered paid purchase.               |
| `shop.on_declined(fn)`         | Connection         | Called when the player said no or did not answer.        |

A player or a uuid string works wherever a player is taken.

## Delivery: `on_paid`

```luau
shop.on_paid(function(purchase)
    -- Hand the item over here. Returning without an error marks it delivered.
    for _, player in players.list() do
        if player.uuid == purchase.player then player:message("Thanks for buying VIP") end
    end
end)
```

`shop.on_paid` calls `fn({request, player, product})` for each undelivered
paid purchase — `player` is the buyer's uuid, `product` the product's key,
`request` the purchase's own id.

The delivery contract:

- It **runs on the server the player is on**: an experience has many servers,
  and each one hands over only to its own players.
- A purchase for a player who is not online **waits until they join one**.
- **At least one active paid handler must complete successfully, and all
  active paid handlers must succeed, before the purchase is acknowledged.**
- With no paid handler, or if one raises an error, it stays pending.
- An `on_declined` listener alone never acknowledges a paid purchase.

## `on_declined`

```luau
shop.on_declined(function(purchase)
    -- The player said no, or did not answer. Close the pack's own shop screen.
end)
```

`shop.on_declined` calls `fn({request, player, product})` when the player
said no or did not answer. It sees the same purchase shape as `on_paid`.

## Retries and idempotence

**Delivery can repeat after a failure or restart: use `purchase.request` as a
durable idempotency key when granting a reward.** Record the request id in
[shared stores](/systems/shared-stores/) or [storage](/systems/storage/) before
granting, so a repeated delivery does not grant twice.

The same error discipline as stores applies:

- After an error, read again.
- After an I/O timeout, a write may have committed. **Retry only versioned
  writes, never an increment.**
- A world release rollback does not rewind shared facts or blobs.

## Product keys

A product key is **1 to 32 characters of `a-z`, `0-9`, `_` and `-`**. Another
key is an error.

## Where the shop exists

Calls yield, like `stores` — call them from scripts, callbacks or tasks, not
from synchronous ask handlers or module initialization.

:::caution[Gotcha]
only experiences in the Minefort Creator Rewards Program have
the shop. Elsewhere, and in local runs, `prompt` returns nil and `owns`
returns false — code written against the shop degrades, it does not error.
:::

## Portals: rent and point

On the experience grounds, `hub.rent(player, slot, product, experience)`
offers a portal for Gems **like `shop.prompt`**: it returns a request id or
nil, and **`shop.on_paid` hands the purchase over**. `hub.point` turns the
player's own live portal for free. See [Hub](/systems/hub/#portals-rent-and-point).

## See also

- [Hub](/systems/hub/) — `hub.rent` and `hub.point`, the portal calls that flow
  through the shop.
- [Shared stores](/systems/shared-stores/) — versioned writes for idempotent
  delivery.
- [Menus](/ui/menus/) — a pack's own shop screen to close on decline.
- [`ShopPurchase`](/ref/ShopPurchase/) — the reference entry for the purchase
  table.
