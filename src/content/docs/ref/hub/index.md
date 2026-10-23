---
title: 'hub global'
description: 'The Minefort hub: servers, experiences and portals.'
---

The Minefort hub: servers, experiences and portals.

Part of the [Storage](/systems/storage/) article.

## Functions

| Call | Purpose |
| --- | --- |
| [`servers`](/ref/hub/servers/) | The players' servers that are online, and the published experiences (`category == "experience"`). `id` is what `player:connect` takes. |
| [`experiences`](/ref/hub/experiences/) | The portals of the experience grounds. `experience` is what `/play` takes. |
| [`hubs`](/ref/hub/hubs/) | Every hub that is online, this one included. `id` is what `player:connect` takes. |
| [`rent`](/ref/hub/rent/) | Offers portal `slot` for Gems, to lead to `experience` (what `/play` takes). Returns the request id, or nil. More time on your own portal may leave `experience` out. |
| [`point`](/ref/hub/point/) | Turns the player's own live portal to another published experience. |
