# SOURCE: Rooms

```luau
local room = rooms.create{
    spawn_point = vec3(0.5, 65, 0.5),
    generate = function(chunk) chunk:fill(chunk.min, chunk.min + vec3(15, 0, 15), "stone") end,
}
player:move_to(room)          -- the client swaps worlds in place
room.ui.title{ title = "Welcome" }
room:message("A new round starts")   -- a chat line to everyone in this room
room.players.on_join(function(p) end)  -- fires after move_to as well
print(player.room == room)    -- rooms compare by identity; `player.room` is nil while moving
room:destroy()                -- when the last player left; players still in it keep the world
```
- The global `players.on_join` fires on connect, in the main room. A room’s
own fires on each move in. `players.on_leave` matches.
## Spawn points
`spawn_point` is the position where a player arrives. `spawn` is never a
position: it is the call `world.spawn` and the switch of an entity kind.
```luau
print(world.spawn_point)    -- this room's point
world.spawn_point = vec3(8.5, 66, 8.5)    -- move it
room.spawn_point = vec3(0.5, 80, 0.5)    -- the same field of a different room
player.spawn_point = vec3(20.5, 65, -7.5)    -- this player respawns here
print(player.spawn_point)    -- vec3, or nil for the room's point
player.spawn_point = nil    -- the room's point again
```
- `citadel.yml` has `spawn_point: [x, y, z]` for the main room.
`rooms.create { spawn_point = vec3(..) }` sets it for a new room.
- A write to `world.spawn_point` or `room.spawn_point` changes where a player
arrives: on a join, on a respawn, and on a move to the room. The clients in
the room get the new compass target.
- The write is not stored. After a restart the room has the point of
`citadel.yml` or of the stored world again.
- The write does not move the chunks that stay loaded, the spawn protection,
or the area where no mob spawns by itself. Those stay at the first point.
- `player.spawn_point` is the player’s own respawn point. A bed sets the same
value where the game has beds. A point that a pack sets needs no bed. The
engine keeps the block of the position: `vec3(20.2, 65, -7.9)` reads back as
`vec3(20.5, 65, -7.5)`.
- `player.spawn_point = nil` also removes a point that a bed set.
- Manifest keys and `rooms.create` options are checked: an unknown key is
an error naming the field and the accepted keys.
