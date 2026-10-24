---
title: "shop.on_declined"
description: "Called when the player said no or did not answer."
---

Part of [`shop`](/ref/shop/).

```luau
shop.on_declined(handler: (purchase: ShopPurchase) -> ()) → Connection
```

Called when the player said no or did not answer.

## Parameters

| Name      | Type                              | Required |
| --------- | --------------------------------- | -------- |
| `handler` | `(purchase: ShopPurchase ) -> ()` | yes      |

## Returns

- [`Connection`](/ref/Connection/)

## Used in

> "shop.on_declined(function(purchase)" — [Shop](/systems/shop/)
> "- `shop.on_declined(fn)` calls `fn({request, player, product})` when the player said no or did not answer." — [Shop](/systems/shop/)
