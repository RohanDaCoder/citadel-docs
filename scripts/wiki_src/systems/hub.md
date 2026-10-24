---
title: Hub
section: systems
order: 7
description: What Minefort tells its own hub — hub.servers, hub.experiences and hub.hubs with their fields, hub.role ranks and hub.online, banners read through the http cache, and the rent/point portal calls.
tags: [hub, servers, experiences, portals, ranks, banners]
---

# Hub

> **In short:** `hub` is what Minefort tells its own hub: the servers that
> are online, the experience portals of the grounds, the other hubs, player
> ranks and the network's online count. The lists refresh every minute; the
> first call waits up to two seconds for them, so call it from a task. This
> page covers the three list calls with their exact fields, ranks, banners
> and the portal calls `hub.rent` and `hub.point`.

## The calls

```luau
task.spawn(function()
    for _, s in hub.servers() do print(s.name, s.players) end
    for _, e in hub.experiences() do print(e.slot, e.experience) end
    for _, h in hub.hubs() do print(h.name, h.players) end
    print(hub.online())
end)
```

| Call                                           | Returns    | Purpose                                                          |
| ---------------------------------------------- | ---------- | ---------------------------------------------------------------- |
| `hub.servers()`                                | list       | The players' servers that are online, and published experiences. |
| `hub.experiences()`                            | list       | The portals of the experience grounds.                           |
| `hub.hubs()`                                   | list       | Every hub that is online, this one included.                     |
| `hub.role(player)`                             | string     | The player's rank on Minefort, or nil.                           |
| `hub.online()`                                 | number     | How many players are online on the whole of Minefort, or nil.    |
| `hub.rent(player, slot, product, experience?)` | request id | Offers a portal of the grounds for Gems.                         |
| `hub.point(player, slot, experience)`          | boolean    | Turns the player's own live portal.                              |

**Anywhere but a hub, the lists are empty and both the ranks and the total
are nil** — the calls work, they just have nothing to say.

## `hub.servers()`

Returns a list of the servers that are online:

| Field                   | Meaning                                                    |
| ----------------------- | ---------------------------------------------------------- |
| `id`                    | What `player:connect` takes.                               |
| `name`                  | The server's name.                                         |
| `category`              | Its category; `"experience"` marks a published experience. |
| `motd`                  | Its message of the day; for an experience, its pitch.      |
| `icon`                  | Its icon, or nil.                                          |
| `banner`                | The URL of its banner, or nil.                             |
| `players`, `maxPlayers` | Who is on it, and its cap.                                 |

A field Minefort does not know is nil. **An entry with
`category = "experience"` is a published experience**: its `id` is the name
`/play` takes, `motd` its pitch, and `banner` the URL of its banner, or nil.

## `hub.experiences()`

Returns a list of `{slot, experience, title, pitch, icon, banner, players}` —
the portals of the experience grounds:

| Field            | Meaning                              |
| ---------------- | ------------------------------------ |
| `slot`           | The portal's slot.                   |
| `experience`     | The name `/play` takes.              |
| `title`, `pitch` | What the portal shows.               |
| `icon`, `banner` | Artwork, or nil.                     |
| `players`        | How many players the experience has. |

A slot that is not in the list has no experience.

## `hub.hubs()`

Returns a list of `{id, name, players, region}`, one per hub that is online,
this one included. `player:connect(id)` sends a player to that hub.

## Ranks and the online count

`hub.role(player)` returns the player's rank on Minefort — `"owner"`,
`"admin"`, `"moderator"` or `"builder"` — and nil for everyone else. It also
takes a uuid, with or without dashes. `hub.online()` returns how many players
are online on the whole of Minefort, or nil before Minefort has said.

Minefort sends the ranks and the total **every minute**. Anywhere but a hub,
both are nil. A new rank reaches the hub within one minute.

> **Note:** `hub.role` is Minefort-wide — the ranks of the platform, not of
> this server. The server's own all-permissions list is `operators` in
> [server settings](/wiki/server-settings).

## Reading a banner

A `banner` is a 1024×512 PNG its creator uploaded and Minefort checked:
**8 by 4 maps**. Read it with the HTTP cache — a new banner has a new URL, so
the cache never shows an old one:

```luau
local image = http.get(banner, { cache = 86400 }):image()
```

See [HTTP](/wiki/http#the-cache) for `cache` and `:image()`.

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

Minefort keeps the lists up to date. **The first call of `servers`,
`experiences` or `hubs` waits at most two seconds for them, so call it from a
task** — the opening example wraps all four calls in `task.spawn`.

## See also

- [Shop](/wiki/shop) — `on_paid` delivers what `hub.rent` sells.
- [HTTP](/wiki/http) — banners through the cache and `:image()`.
- [Network](/wiki/network) — instances, the other kind of server
  `player:connect` reaches.
- [Permissions](/wiki/permissions) — the server's own operator and
  permission model.
