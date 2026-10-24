---
title: "Teleport pads"
description: "Three ways to move players between places — world.zone trigger pads in a room, routes between dimensions with a standing trigger, and commands for explicit travel."
---

:::note[In short]
inside one room, a pad is a `world.zone` with `on_enter`.
Between dimensions, a `routes.add` trigger moves the player when they stand
in a block. And `/spawn`-style commands move players explicitly. All three
patterns come straight from the docs' own examples.
:::

## Pattern 1: a zone pad in a room

```luau
local goal = world.zone{
    from = vec3(10, 64, 10), to = vec3(14, 66, 14),
    on_enter = function(player)
        message(player.name .. " scored", colors.lime)
    end,
    on_leave = function(player) end,
}
```

The rules that make a zone a good pad:

- `from` and `to` are block positions, in either order, both corners inside.
- A player is inside when their **feet** are.
- Disconnecting inside a zone runs `on_leave`.
- A zone ends with the script — re-create it on reload.
- `goal:contains(player)` and `goal:players()` answer "is someone in it now".

To teleport on entry rather than just score:

```luau
world.zone{
    from = vec3(-2, 64, -2), to = vec3(2, 66, 2),
    on_enter = function(player)
        player:teleport(world.spawn_point)
    end,
}
```

`player:teleport(pos)` keeps the way the player faces when you leave the
rotation out.

## Pattern 2: a route between dimensions

The dungeon guide's gate — step on the carpet, arrive in the dungeon:

```luau
routes.add{
    from = "overworld",
    to = "dungeon",
    trigger = { block = "light_blue_carpet" },
    placement = { x = 7.5, y = 64, z = 7.5 },
}
```

- `trigger = { block = "light_blue_carpet" }` fires on the first tick a
  player stands in the block; `ticks = 80` makes them wait, as a Nether
  portal does.
- `placement` is where they arrive; leave it out for the dimension's spawn.
- After a trip a player must step out of the trigger block for half a second
  before it can fire again.

The way back is a command with `player:travel`:

```luau
commands.add("leave", function(player)
    player:travel("overworld")
end)
```

The full walkthrough is [A dungeon dimension](/guides/guide-a-dungeon-dimension/).

## Pattern 3: proximity pads

For "everyone within N blocks", skip the zone and use `players.near` on a
tick or timer:

```luau
local conn = time.every(0.5, function()
    for _, p in players.near(vec3(0, 65, 0), 4) do
        p:teleport(vec3(0.5, 80, 0.5))
    end
end)
```

- `players.near(pos, 8)` — every player within eight blocks of a point.
- `players.within(from, to)` — every player inside a box of blocks, corners
  included.
- Cancel with `conn:cancel()` when the pad closes.

## Choosing the pattern

| Need                                         | Use                          |
| -------------------------------------------- | ---------------------------- |
| Move within the room, by area                | `world.zone` with `on_enter` |
| Move between the group's worlds, by standing | `routes.add` with a trigger  |
| Move between the group's worlds, on demand   | `player:travel(dim, pos)`    |
| Move within the room, by command             | `player:teleport(pos)`       |
| Effect on everyone near a point              | `players.near` on a timer    |

## See also

- [Rooms and dimensions](/concepts/rooms-and-dimensions/) — zones' neighbours:
  spawn points, rooms, travel.
- [Zones and raycasts](/world/world-state/) — the full zone API in context.
- [Movement](/players/movement/) — teleport, rotation, `move_to`.
