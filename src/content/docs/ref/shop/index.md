---
title: "shop global"
description: "Minefort's Gem shop: prompts, ownership and paid delivery."
---

Minefort's Gem shop: prompts, ownership and paid delivery.

Part of the [Storage](/systems/storage/) article.

## Functions

| Call                                    | Purpose                                                                                                                        |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| [`prompt`](/ref/shop/prompt/)           | Asks Minefort to offer `product` to the player. Returns the request id, or nil when it was not offered.                        |
| [`owns`](/ref/shop/owns/)               | Whether the player owns this pass.                                                                                             |
| [`on_paid`](/ref/shop/on_paid/)         | Called once per paid purchase; returning without an error hands it over. An error leaves it waiting, to be called again later. |
| [`on_declined`](/ref/shop/on_declined/) | Called when the player said no or did not answer.                                                                              |
