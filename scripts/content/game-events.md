---
title: "Game events"
url: /docs/citadel/game-events
---

# Game events

```luau
world.on_block_break(function(player, pos, block) end) -> connection
world.on_block_place(function(player, pos, block) end) -> connection
--   block is the canonical name: what was there for a break, what was put
--   down for a place
world.on_entity_spawn(function(entity, name) end) -> connection   -- a mob appeared; entity is the handle
world.on_entity_death(function(id, name) end) -> connection    -- a mob died; it is gone, so id and name is all there is
players.on_pickup(function(player, item, count) end) -> connection
players.on_drop(function(player, item, count) end) -> connection

```
`player` is `nil` when:
- the world dropped the stack (a leaf decays, a mob dies, an explosion);
- the player has already left the room.
```luau
world.on_block_break(function(player, pos, block)
    if block == "diamond_ore" and player then
        message(player.name .. " struck diamond", colors.cyan)
    end
end)

```
`world.on_entity_spawn` fires for mob kinds only. `world.on_entity_death`
fires for mob kinds and for a pack’s living body (`physics = "living"`). They
do not fire for an arrow, an item or another pack kind.
On a `mode: lite` server, `world.spawn` of a mob kind fires `world.on_entity_spawn`. A mob
that spawns by itself (its kind has `spawn = true`) fires it on every game
version that has natural spawning (a0.1.4 and later). A spider jockey fires
it two times: for the spider, then for its rider.
