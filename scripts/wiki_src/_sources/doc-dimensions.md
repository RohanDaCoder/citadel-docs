# SOURCE: Dimensions

```yaml
dimensions:
  dungeon:                          # castle:dungeon, saved to world_dungeon
    type: { has_skylight: false, has_ceiling: true, weather: false }
    world: script                   # or void
```
- `type` fields, all optional and starting from the main world’s:
`has_skylight`, `has_ceiling`, `weather`, `ultrawarm`, `bed_works`,
`respawn_anchor_works`, `coordinate_scale`, `fixed_time`, `effects`.
- A trigger block fires after `ticks` ticks standing in it (1 by default);
after a trip the player steps out for half a second before it fires again.
- A player’s inventory and health go with them; their file stays the main
world’s. Dying anywhere respawns them in the main world.
