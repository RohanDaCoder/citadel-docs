---
title: Rooms and dimensions
section: concepts
order: 6
description: Two ways to have more than one world — rooms, made at runtime with rooms.create and each with its own world/players/ui/game tables, and dimensions, declared in citadel.yml and reached by routes and player:travel.
tags: [rooms, dimensions, routes, travel, worlds]
---
# Rooms and dimensions

> **In short:** a **room** is a runtime world the script makes with
> `rooms.create{}` — a player swaps to it in place, and it gets its own
> `world`/`players`/`ui`/`game` tables. A **dimension** is a manifest-declared
> world of the server's group, saved to its own folder and reached by
> `routes.add` or `player:travel`. Rooms are for instances (a minigame, a
> per-player course); dimensions are for places (a dungeon, a nether).

## Rooms

```luau
local room = rooms.create{
    spawn_point = vec3(0.5, 65, 0.5),
    generate = function(chunk) chunk:fill(chunk.min, chunk.min + vec3(15, 0, 15), "stone") end,
}
player:move_to(room)          -- the client swaps worlds in place
room.ui.title{ title = "Welcome" }
room:message("A new round starts")   -- a chat line to everyone in this room
room.players.on_join(function(p) end)  -- fires after move_to as well
print(player.room == room)    -- rooms compare by identity; nil while moving
room:destroy()                -- when the last player left; players still in it keep the world
```

The rules:

- The global `players.on_join` fires on connect, in the main room. A room's
  own fires on each move in. `players.on_leave` matches.
- A room made by `rooms.create` runs no survival rules and no natural mob
  spawning by default (as a lite world).
- Destroy a room when the last player leaves it; players still in it keep the
  world until they go.
- Per-room game settings: `room.game.entities.cow.spawn = true` is that room's
  own value.

### A world per player

The per-player-instance pattern — `/play` builds a course in a room that
belongs to one player:

```luau
local COURSE = { vec3(0, 65, 4), vec3(4, 66, 8), vec3(-3, 68, 12) }

world.on_generate(function(chunk)
    chunk:fill(vec3(chunk.min.x, 64, chunk.min.z), vec3(chunk.max.x, 64, chunk.max.z), "stone")
end)

players.on_join(function(player)
    player.ui.title{ title = "Lobby", subtitle = "type /play", color = colors.cyan }
end)

commands.add("play", function(player)
    local mine = rooms.create{
        spawn_point = vec3(0.5, 65, 0.5),
        generate = function(chunk)
            chunk:fill(vec3(chunk.min.x, 64, chunk.min.z), vec3(chunk.max.x, 64, chunk.max.z), "stone")
            for _, at in COURSE do
                chunk:set(at, "gold_block")
            end
        end,
    }
    mine.players.on_join(function(p)
        p:message("Reach every gold block.", colors.yellow)
        mine.ui.title{ title = "Go", color = colors.lime }
    end)
    mine.players.on_leave(function()
        if mine.players.count() == 0 then mine:destroy() end   -- the last one out closes it
    end)
    player:move_to(mine)
end)
```

The full tutorial is [Parkour, a room each](/wiki/guide-parkour-a-room-each).

## Dimensions

A pack adds a world in `citadel.yml`, under `dimensions:`. The name is its id
inside the pack, so `dungeon` under pack `castle` is `castle:dungeon`:

```yaml
dimensions:
  dungeon:
    type: { has_skylight: false, has_ceiling: true, weather: false }
    world: script            # or "void" to leave chunks empty
```

- `type` says how the world behaves. Every field is optional and starts from
  the main world's: `has_skylight`, `has_ceiling`, `weather`, `ultrawarm`,
  `bed_works`, `respawn_anchor_works`, `coordinate_scale`, `fixed_time` and
  `effects`.
- A world with a roof looks like the Nether to a client, one with no sky and
  no roof like the End. `effects` chooses one of the three yourself.
- A dimension is a world of the server's group: it ticks after the main world
  and saves to `world_dungeon` beside it.

`world.dimension(name)` is that world's own `world` table, by dimension id or
its last part (`"dungeon"`, `"minecraft:the_nether"`):

```luau
local dungeon = world.dimension("dungeon")
dungeon.on_generate(function(chunk)
    chunk:fill(vec3(chunk.min.x, 63, chunk.min.z), vec3(chunk.max.x, 63, chunk.max.z), "bedrock")
    chunk:fill(vec3(chunk.min.x, 64, chunk.min.z), vec3(chunk.max.x, 68, chunk.max.z), "mossy_cobblestone")
end)
```

## Routes between worlds

A route is how a player gets from one world to another, with a trigger:

```luau
routes.add{
    from = "overworld",
    to = "dungeon",
    trigger = { block = "light_blue_carpet" },
    placement = { x = 7.5, y = 64, z = 7.5 },
}
```

- `trigger = { block = "light_blue_carpet" }` fires on the first tick a
  player stands in the block. `ticks = 80` makes them wait, as a Nether
  portal does.
- `placement` is where they arrive; leave it out for the dimension's spawn.
- After a trip, a player must step out of the trigger block for half a second
  before it can fire again.

`player:travel(dimension, pos)` sends a player to any world of the group, at
`pos` or its spawn — the command version of a route:

```luau
commands.add("leave", function(player)
    player:travel("overworld")
end)
```

## Spawn points, precisely

- `spawn_point` is the position where a player arrives. `spawn` is never a
  position: it is the call `world.spawn` and the switch of an entity kind.
- `citadel.yml` has `spawn_point: [x, y, z]` for the main room;
  `rooms.create { spawn_point = vec3(..) }` sets it for a new room.
- A write to `world.spawn_point` or `room.spawn_point` changes where a player
  arrives — on a join, on a respawn, and on a move to the room — and the
  clients in the room get the new compass target.
- The write is **not stored**: after a restart the room has the point of
  `citadel.yml` or of the stored world again.
- The write does not move the chunks that stay loaded, the spawn protection,
  or the area where no mob spawns by itself. Those stay at the first point.
- `player.spawn_point` is the player's own respawn point. A bed sets the same
  value where the game has beds; a point a pack sets needs no bed. The engine
  keeps the block of the position: `vec3(20.2, 65, -7.9)` reads back as
  `vec3(20.5, 65, -7.5)`. `player.spawn_point = nil` also removes a point a
  bed set.
- Manifest keys and `rooms.create` options are checked: an unknown key is an
  error naming the field and the accepted keys.

## See also

- [Pack anatomy](/wiki/pack-anatomy) — the manifest's `dimensions` key.
- [A dungeon dimension](/wiki/guide-a-dungeon-dimension) — the full tutorial.
- [Architecture](/wiki/architecture) — rooms and per-room tables.
- [Game data](/wiki/game-data) — per-room registry settings.
