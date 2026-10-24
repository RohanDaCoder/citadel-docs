---
title: "player:connect"
description: 'Asks Minefort to move the player to another server by name: an instance''s id, the network''s name (its default member) or "hub"'
---

Part of [`Player`](/ref/Player/).

```luau
player:connect(server: string)
```

Asks Minefort to move the player to another server by name: an instance's `id`, the network's name (its default member) or "hub". Minefort decides and does not answer; a player still here was not moved.

## Parameters

| Name     | Type     | Required |
| -------- | -------- | -------- |
| `server` | `string` | yes      |

## Used in

> "player:connect("hub") -- ask Minefort to move them to another server, by its name" — [Body and movement](/players/movement/)
> "- `player:connect(server)` asks Minefort's proxy to move the player: a BungeeCord `Connect` for a Java player, a `Transfer` to that name for a Bedrock player. It returns nothing and does not yield." — [Body and movement](/players/movement/)
> "player:connect(arena.id)" — [Network](/systems/network/)
> "for _, player in waiting[instance.id] or {} do player:connect(instance.id) end" — [Network](/systems/network/)
> "- `hub.servers()` returns a list of `{id, name, category, motd, icon, banner, players, maxPlayers}`. `id` is what `player:connect` takes. A field Minefort does not know is nil. An entry with `category = "experience"` is a published experience: its `id` is the name `/play` takes, `motd` its pitch, and `banner` the URL of its banner, or nil." — [Hub](/systems/hub/)
> "- `hub.hubs()` returns a list of `{id, name, players, region}`, one per hub that is online, this one included. `player:connect(id)` sends a player to that hub." — [Hub](/systems/hub/)
