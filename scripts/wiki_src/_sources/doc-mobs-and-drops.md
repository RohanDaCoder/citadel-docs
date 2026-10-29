# SOURCE: Mobs and drops

```luau
local cow = world.spawn("cow", vec3(4.5, 65, 8.5))    -- nil where this game has no such kind
cow.id    -- entity id, what players.on_click reports in hit.entity_id
cow.name    -- "cow"
cow.at    -- vec3, live; nil once it is gone
cow.rotation, cow.hostile
cow.health, cow.max_health    -- its health now, and the most its kind gives it
cow.alive    -- is it still in the world
cow:destroy()    -- takes it out on the next tick
world.entities { mob = true }    -- every mob in this room, as handles
world.entities { mob = false }    -- every entity that is not a mob
world.items()    -- the stacks on the ground: { { id, item = "dirt", count = 3, at = vec3 }, ... }
```
- A mob acts on its own on both kinds of server, lite included.
- Each read gets the entity’s current state. Check `alive`.
- A mob a pack spawns stays when the script reloads. An NPC does not.
- `tostring(cow)` is `entity(cow, 7)`: the kind’s name and the id.
- A mob has the **same handle** as every entity the world moves: `cow.velocity`, `cow:push(v)` and `cow:nearby(8)` work too. See “Custom entities”.
> **a0.1.0 spawns nothing on its own.** On an Alpha world every entity in
`world.entities { mob = true }` comes from a dungeon spawner, `/summon` or this call.
**a0.1.0 spawns nothing on its own.** On an Alpha world every entity in
`world.entities { mob = true }` comes from a dungeon spawner, `/summon` or this call.
