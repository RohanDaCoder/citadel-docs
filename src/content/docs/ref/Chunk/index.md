---
title: 'Chunk type'
description: 'A 16 by 16 column of blocks, handed to world.on_generate, world.on_populate and a room''s generate to fill.'
---

A 16 by 16 column of blocks, handed to `world.on_generate`, `world.on_populate` and a room's `generate` to fill.

## Functions

| Call | Purpose |
| --- | --- |
| [`get`](/ref/Chunk/get/) | Chunk X coordinate (16 blocks each). Chunk Z coordinate (16 blocks each). The chunk's lowest corner, inclusive; y runs 0..255 or the game version's height. The chunk's highest corner, inclusive. Returns the block there now, by name; air outside the chunk. |
| [`set`](/ref/Chunk/set/) | Sets one block; positions outside the chunk are ignored. |
| [`fill`](/ref/Chunk/fill/) | Fills a box of blocks, clipped to the chunk. |
| [`paste`](/ref/Chunk/paste/) | Clipped to this chunk; air is skipped unless `air` is true. `part` names the paste for `citadel render --part` and `citadel check`; the build's own `b:part`s are then inside it ("house/roof"). |
| [`get_biome`](/ref/Chunk/get_biome/) | Returns the biome of the column at `pos`, by name; `nil` outside the chunk. A biome belongs to a column, so `pos.y` is not read. |
| [`set_biome`](/ref/Chunk/set_biome/) | Sets the biome of one column: a vanilla name ("desert") or the name `game.biomes.define` returned. |
| [`fill_biome`](/ref/Chunk/fill_biome/) | Sets the biome of every column in a box, clipped to the chunk. |
