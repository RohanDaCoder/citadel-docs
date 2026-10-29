---
title: 'world global · type World'
description: 'A room''s blocks, entities, displays, screens and time: the world global, or room.world.'
---

A room's blocks, entities, displays, screens and time: the `world` global, or `room.world`.

Part of the [Terrain generation](/world/terrain-generation/) article.

## Functions

| Call | Purpose |
| --- | --- |
| [`on_generate`](/ref/World/on_generate/) | Called for a chunk each time it comes into memory, in a script world; it must make the same blocks every time. |
| [`on_populate`](/ref/World/on_populate/) | Each chunk the overworld terrain made, once, after it made it. |
| [`dimension`](/ref/World/dimension/) | Another world of the server's group, by dimension id or its last part ("dungeon", "minecraft:the_nether"): that world's own `world` table. |
| [`drop`](/ref/World/drop/) | A stack on the ground at a block, as a broken block leaves one. |
| [`container`](/ref/World/container/) | A chest's stacks, or nil where the block keeps none. |
| [`rules`](/ref/World/rules/) | `world.rules{ fall = true }` switches one on, false off; a rule left out or nil keeps its value, and a number or a string is an error. `world.rules()` reads them. |
| [`raycast`](/ref/World/raycast/) | The first block a ray from `from` along `direction` meets within `max` blocks, and the face it came in through; nil for none. |
| [`sees`](/ref/World/sees/) | True when no block stops the line from `from` to `to`: a block with a collision box does (glass, leaves), water and grass do not. |
| [`raycasts`](/ref/World/raycasts/) | `n` lines at once. `rays` holds six f64 a line (from x, y, z, to x, y, z); `out` gets one f64 a line: how far along it the first block is that stops it, or -1 for a clear line. |
| [`light_at`](/ref/World/light_at/) | Block light and sky light, 0 to 15, and whether nothing above holds off the sky. |
| [`path`](/ref/World/path/) | The points a body walks from `from` to the block at `to`, or nil. The game's own search: a step up of one block, falls of `fall` (3). `size` is { width, height } (0.6, 1.8); `swim` goes through water; `range` (the distance + 16) and `budget` (2000 nodes) stop a long search, which then gives the part that came closest. |
| [`zone`](/ref/World/zone/) | Makes a box of blocks, both corners included, that knows who is in it; checked once a tick by feet position. Ends with the script. |
| [`set_block`](/ref/World/set_block/) | `skin` is for "player_head" and "player_wall_head" only: an account's name, or the raw `textures` property. |
| [`set_blocks`](/ref/World/set_blocks/) | Sets many blocks at once, live, stored and sent; the cheapest way. A row takes `skin` too, for a player head. |
| [`fill`](/ref/World/fill/) | Fills a box of blocks between two corners, live, stored and sent to everyone. |
| [`schematic`](/ref/World/schematic/) | A file inside the pack; a path that leaves it, or one that is not there, is an error naming the file. |
| [`build`](/ref/World/build/) | The same value, written in code instead of read from a file. `{ detail = 2 }`: coordinates are half blocks, fitted to slabs and stairs. |
| [`paste`](/ref/World/paste/) | Live, stored and sent; air is skipped unless `air` is true. |
| [`get_block`](/ref/World/get_block/) | `nil` where that chunk is not in memory: a read never generates. |
| [`block`](/ref/World/block/) | The block there as the handle a hook gets: reads are live, and what it does lands on the next tick. `state` and `data` are for this pack's own blocks. `nil` where that chunk is not in memory. |
| [`get_biome`](/ref/World/get_biome/) | Returns the biome name of the column at `pos`; `nil` where that chunk is not in memory. |
| [`generate`](/ref/World/generate/) | Declares this world: the engine makes each chunk from the rules, on every core, and no script runs for a chunk. |
| [`get_blocks`](/ref/World/get_blocks/) | A box, in x, then z, then y order. |
| [`items`](/ref/World/items/) | The stacks on the ground: `{ id, item, count, at }` rows. |
| [`spawn`](/ref/World/spawn/) | Puts an entity at a point and returns its handle. A mob kind of the game by name (`world.spawn("cow", pos)`) is the game's own entity, and takes no `data`. A pack's own kind takes the data it starts life holding. `nil` for a kind nothing defined and this game does not have. |
| [`entities`](/ref/World/entities/) | Live and queued entities, in ascending id. Optional near/radius select a sphere; kind filters by canonical name. near and radius go together. `mob = true` gives the mobs only, `mob = false` the rest. |
| [`explode`](/ref/World/explode/) | A blast at a point. The power is clamped by this game's own column and the tick's explosion budget decides when it goes off, never whether. |
| [`on_block_break`](/ref/World/on_block_break/) | What the survival tick did. Observe-only: the world has already changed, and what the callback returns is not read. |
| [`on_block_place`](/ref/World/on_block_place/) | Tells after a block was placed, with its canonical name. Observe-only; `player` is nil when nobody placed it or they left. |
| [`on_entity_spawn`](/ref/World/on_entity_spawn/) | Tells after a mob appeared, with its handle and name; a natural spawn fires it on every game version that has one, and a pack's own `world.spawn("cow", pos)` fires it too. Mob kinds only. |
| [`on_entity_death`](/ref/World/on_entity_death/) | Tells after a mob died; it is gone, so its id and name is all there is. Mob kinds only. |
| [`time`](/ref/World/time/) | Holds the sky at a time (ticks, or "sunrise", "day", "noon", "sunset", "night", "midnight"), or asks a function each tick, `s` seconds after the call. With no argument: the time of day now, 0 to 23999. |
| [`light`](/ref/World/light/) | Sends players light no block makes, 1 to 15 a source; each call replaces the last, `{}` ends it. 1.14 and later. |
| [`screen`](/ref/World/screen/) | Puts a wall of map frames, `width` by `height` frames (128 pixels each), in front of a wall; `at` is the top-left frame. Returns a Screen. |
| [`canvas`](/ref/World/canvas/) | Makes a picture of `width` by `height` maps (1 by 1 by default, 16 at most a side) with no frame of its own, for a frame, a hand or a screen. |
| [`display`](/ref/World/display/) | A model stands in the world through the same call as everything else, and is the one kind that hands back something other than a Display. |
| [`hitbox`](/ref/World/hitbox/) | Makes an invisible box a player can click; `solid` also makes it a wall. `depth` is the width unless given. 1.19.4 and later. |
| [`npc`](/ref/World/npc/) | Places a player-shaped entity every client from 1.8 sees; removed when the script ends or reloads. |
| [`puppet`](/ref/World/puppet/) | Places a mob's body with no mind of its own that the script moves; its name tag always shows. An error when this game has no such mob kind. |

## Fields

| Field | Purpose |
| --- | --- |
| [`world.spawn_point: Vec3`](/ref/World/spawn_point/) | Where players arrive in this room; writable. The same value as the room's `spawn_point`. |
