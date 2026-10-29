---
title: 'Hub'
description: 'What Minefort tells its own hub — hub.experiences and the banner fields, hub.role ranks, and the rent/point portal calls; the server lists moved to network.browse, network.instances and network.online.'
---

:::note[In short]
`hub` is what Minefort tells its own hub: the experience
portals of the grounds, player ranks, and the `rent` and `point` calls for
live portals. The server lists are not the hub's any more — the hub browses
them with [`network.browse`](/ref/network/browse/), its hubs and always-on
servers with [`network.instances`](/ref/network/instances/), and asks the
player count with [`network.online`](/ref/network/online/). The lists refresh
every minute; the first call of `experiences` waits up to two seconds for
them, so call it from a task. This page covers the calls with their exact
fields, ranks, banners and the portal calls `hub.rent` and `hub.point`.
:::

## The calls

```luau
task.spawn(function()
    for _, s in network.browse('featured') or {} do print(s.name, s.players) end
    for _, e in hub.experiences() do print(e.slot, e.experience) end
    for _, h in network.instances() or {} do print(h.name, h.players) end
    print(network.online())
end)
```

| Call | Returns | Purpose |
| --- | --- | --- |
| `hub.experiences()` | list | The portals of the experience grounds. |
| `hub.role(player)` | string | The player's rank on Minefort, or nil. |
| `hub.rent(player, slot, product, experience?)` | request id | Offers a portal of the grounds for Gems. |
| `hub.point(player, slot, experience)` | boolean | Turns the player's own live portal. |
| `network.browse(view, options?)` | rows, total | Finds other networks. Hub only. |
| `network.instances(label?)` | list | The network's always-on servers and hubs. |
| `network.online(label?)` | number | How many play on this network. |

**Anywhere but a hub, the lists are empty and the ranks are nil** — the calls
work, they just have nothing to say.

## `hub.experiences()`

Returns a list of `{slot, experience, title, pitch, icon, banner, players}` —
the portals of the experience grounds:

| Field | Meaning |
| --- | --- |
| `slot` | The portal's slot. |
| `experience` | The name `/play` takes. |
| `title`, `pitch` | What the portal shows. |
| `icon`, `banner` | Artwork, or nil. |
| `players` | How many players the experience has. |

A slot that is not in the list has no experience.

## The server lists live on `network`

`hub` no longer lists servers or hubs. The hub reads them through the
`network` calls — all documented on [Network](/systems/network/):

- [`network.browse(view, options?)`](/ref/network/browse/) finds other
  networks: `"featured"` (the busiest), `"search"`, `"for-you"` and
  `"recent"`. Each row is a network — `{id, name, category, motd, icon,
  players, maxPlayers, state}` — and `id` is what `player:connect` takes.
- [`network.instances()`](/ref/network/instances/) returns this network's
  servers that run all the time — on the platform's hub, the hubs — each
  `{id, name, state, players, region}`, then the network's games started on
  demand.
- [`network.online()`](/ref/network/online/) returns how many play on this
  network: on the platform's hub, everyone on Minefort.

## Ranks

`hub.role(player)` returns the player's rank on Minefort — `"owner"`,
`"admin"`, `"moderator"` or `"builder"` — and nil for everyone else. It also
takes a uuid, with or without dashes.

Minefort sends the ranks **every minute**, so a new rank reaches the hub
within one. Anywhere but a hub, they are nil.

:::note
`hub.role` is Minefort-wide — the ranks of the platform, not of
this server. The server's own all-permissions list is `operators` in
[server settings](/systems/server-settings/).
:::

## Reading a banner

A `banner` is a 1024×512 PNG its creator uploaded and Minefort checked:
**8 by 4 maps**. Read it with the HTTP cache — a new banner has a new URL, so
the cache never shows an old one:

```luau
local image = http.get(banner, { cache = 86400 }):image()
```

See [HTTP](/systems/http/#the-cache) for `cache` and `:image()`.

## Portals: rent and point

- `hub.rent(player, slot, product, experience)` offers a portal of the
  grounds for Gems, **like `shop.prompt`**: `product` is one of the hub's
  rentals, such as `portal_24h`, and `experience` the name `/play` takes of
  any published experience, which the portal then leads to. It returns a
  request id, or nil; **`shop.on_paid` hands the purchase over**. Renting
  your own portal again adds time, and may leave `experience` out to keep
  what it shows.
- `hub.point(player, slot, experience)` turns the player's own live portal
  to another published experience, as often as they like. It returns whether
  it did.

**Minefort decides who may rent or point what:** a stand someone else holds,
or a name that is no published experience, is a no. Anywhere but its hub,
every answer is no.

## Calling from a task

Minefort keeps the lists up to date. **The first call of `experiences` waits
at most two seconds for them, so call it from a task** — the opening example
wraps the list calls in `task.spawn`.

## See also

- [Shop](/systems/shop/) — `on_paid` delivers what `hub.rent` sells.
- [HTTP](/systems/http/) — banners through the cache and `:image()`.
- [Network](/systems/network/) — `browse`, `instances`, `online` and the
  instance events; the other kind of server `player:connect` reaches.
- [Permissions](/players/permissions/) — the server's own operator and
  permission model.
