---
title: 'game global · type Game'
description: 'The game version a room runs, its entity kinds, blocks and items, and the pack''s own blocks, items and recipes: the game global, or room.game.'
---

The game version a room runs, its entity kinds, blocks and items, and the pack's own blocks, items and recipes: the `game` global, or `room.game`.

Part of the [Terrain generation](/world/terrain-generation/) article.

## Functions

| Call | Purpose |
| --- | --- |
| [`block`](/ref/Game/block/) | Returns one block in this version's numbers, or nil for a name this game has no word for. |
| [`item`](/ref/Game/item/) | Returns an item this game has, or nil for a name it does not; never an error. |
| [`texture`](/ref/Game/texture/) | Returns a new texture of width by height pixels, see-through until drawn on, for a pack's block or item. A texture to draw on (512 at most a side), or a PNG file in the pack (4096 at most a side). |

## Fields

| Field | Purpose |
| --- | --- |
| [`game.version: string`](/ref/Game/version/) | This game's version, such as "a0.1.0". |
| [`game.world_height: number`](/ref/Game/world_height/) | How tall the world is in blocks: 128, or 256 for a 1.8.9 world. |
| [`game.sea_level: number`](/ref/Game/sea_level/) | The y of this world's sea level. |
| [`game.entities: Entities & { [string]: (EntityKind \| EntityDef)? }`](/ref/Game/entities/) | The kinds of entity: `define` a pack's own, `amend` the game's own, and read a kind of the game: a mob kind by either spelling (`game.entities.cow`, `game.entities.Cow`), a kind that is not a mob by its name (`game.entities.arrow`); nil where the game has none. It iterates every kind, including pack definitions: `for name, kind in game.entities do`. |
| [`game.blocks: Blocks`](/ref/Game/blocks/) | The one table that *adds* to a version rather than reading it. |
| [`game.biomes: Biomes`](/ref/Game/biomes/) | Biomes of the pack's own: a vanilla biome with other colours and weather. |
| [`game.recipes: Recipes`](/ref/Game/recipes/) | What a crafting grid and a furnace make of a pack's items; recipes are added while the pack loads. |
| [`game.items: Items`](/ref/Game/items/) | Defines items of the pack's own, with a texture for clients from 1.21.4. |
| [`game.terrain: { snow: boolean ?, steps: { TerrainStep }? }?`](/ref/Game/terrain/) | What this world's overworld is made of: `snow` and `steps`, as citadel.yml writes them; read-only, nil when there is no list. |
