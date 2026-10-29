# SOURCE: Dimensions

```yaml
dimensions:
  dungeon:                          # castle:dungeon, saved to world_dungeon
    type: { has_skylight: false, has_ceiling: true, weather: false }
    world: script                   # or void
```
```luau
local dungeon = world.dimension("dungeon")    -- that world's `world` table; "minecraft:the_nether" works too
dungeon.on_generate(function(chunk) chunk:fill(chunk.min, chunk.min + vec3(15, 0, 15), "bedrock") end)
routes.add{ from = "overworld", to = "dungeon", trigger = { block = "light_blue_carpet", ticks = 1 }, placement = { x = 0.5, y = 65, z = 0.5 } }
routes.add{ from = "dungeon", to = "overworld" }    -- no trigger: only player:travel takes it
player:travel("dungeon", vec3(0.5, 65, 0.5))    -- to a point, or without one to its spawn
```
- `type` fields, all optional and starting from the main world’s:
`has_skylight`, `has_ceiling`, `weather`, `ultrawarm`, `bed_works`,
`respawn_anchor_works`, `coordinate_scale`, `fixed_time`, `effects`.
- A trigger block fires after `ticks` ticks standing in it (1 by default);
after a trip the player steps out for half a second before it fires again.
- A player’s inventory and health go with them; their file stays the main
world’s. Dying anywhere respawns them in the main world.
