---
title: 'hub global'
description: 'The Minefort hub: servers, experiences and portals.'
---

The Minefort hub: servers, experiences and portals.

Part of the [Storage](/systems/storage/) article.

## Functions

| Call | Purpose |
| --- | --- |
| [`experiences`](/ref/hub/experiences/) | The portals of the experience grounds. `experience` is what `/play` takes. |
| [`rent`](/ref/hub/rent/) | Offers portal `slot` for Gems, to lead to `experience` (what `/play` takes). Returns the request id, or nil. More time on your own portal may leave `experience` out. |
| [`point`](/ref/hub/point/) | Turns the player's own live portal to another published experience. |
