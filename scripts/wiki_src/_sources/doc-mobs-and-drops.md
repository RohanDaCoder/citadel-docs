# SOURCE: Mobs and drops

- A mob acts on its own on both kinds of server, lite included.
- Each read gets the entity’s current state. Check `alive`.
- A mob a pack spawns stays when the script reloads. An NPC does not.
- `tostring(cow)` is `entity(cow, 7)`: the kind’s name and the id.
- A mob has the **same handle** as every entity the world moves: `cow.velocity`, `cow:push(v)` and `cow:nearby(8)` work too. See “Custom entities”.
> **a0.1.0 spawns nothing on its own.** On an Alpha world every entity in
> `world.entities { mob = true }` comes from a dungeon spawner, `/summon` or this call.
