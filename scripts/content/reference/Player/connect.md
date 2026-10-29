---
title: "player:connect"
url: /docs/citadel/reference/Player/connect
---

# player:connect

Asks Minefort to move the player to another server by name: an instance's `id`, the network's name (its default member) or "hub". Minefort decides and does not answer; a player still here was not moved.

```
player:connect(server: string)
```


## Parameters


## Used in
- [`player:connect("hub") -- ask Minefort to move them to another server, by its name`Body and movement](/docs/citadel/body-and-movement)
- [`- `player:connect(server)` asks Minefort's proxy to move the player: a BungeeCord `Connect` for a Java player, a `Transfer` to that name for a Bedrock player. It returns nothing and does not yield.`Body and movement](/docs/citadel/body-and-movement)
- [`player:connect(arena.id)`Network](/docs/citadel/network)
- [`for _, player in waiting[instance.id] or {} do player:connect(instance.id) end`Network](/docs/citadel/network)
- [`- `hub.servers()` returns a list of `{id, name, category, motd, icon, banner, players, maxPlayers}`. `id` is what `player:connect` takes. A field Minefort does not know is nil. An entry with `category = "experience"` is a published experience: its `id` is the name `/play` takes, `motd` its pitch, and `banner` the URL of its banner, or nil.`Hub](/docs/citadel/hub)
- [`- `hub.hubs()` returns a list of `{id, name, players, region}`, one per hub that is online, this one included. `player:connect(id)` sends a player to that hub.`Hub](/docs/citadel/hub)
