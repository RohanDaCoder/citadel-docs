---
title: Block reference
section: world
order: 2
description: Block naming in Citadel — canonical names without the namespace, [property=value] states in any order and subset, version fallbacks with | alternatives, the write and read calls, player heads with skins, and the detail = 2 half-block system.
tags:
  [
    blocks,
    block-names,
    block-states,
    set-block,
    player-heads,
    detail,
    version-fallbacks,
  ]
---

# Block reference

> **In short:** how a block is named, written, read and substituted. Names are
> Minecraft's canonical names without `minecraft:`; properties go in brackets
> in any order and any subset; every version's blocks are real and stored
> exactly, with nearest-block fallbacks in both directions. Plus the two
> special cases: player heads with skins, and the `detail = 2` half-block
> system inside builds.

## Names

Block names are Minecraft's, without `minecraft:`.

- Every block of every version is real here and stored exactly. An older client
  sees the nearest block its version has.
- Properties go in brackets, in any order and any subset:
  `"oak_trapdoor[facing=east]"`, `"stone_button[facing=west, face=wall]"`.
  Missing properties come from the default state. The nearest state wins.
- A name that is no block of any version (`"grassblock"`, `"stone_brick"`) is
  an error that lists the nearest real names.
- Queries ([`game.block(name)`](/ref/Game/block), the block an entity stands
  on) return `nil` for a name the game lacks.

A block from [`game.blocks.define`](/ref/Blocks/define) works wherever a name
works — its handle or its namespaced name (`"rave:crate"`). See
[Custom blocks](/wiki/custom-blocks).

## Version fallbacks

| Situation                              | What happens                                      |
| -------------------------------------- | ------------------------------------------------- |
| A name this game version lacks         | the nearest block it has — never air              |
| An older client than the block         | the client sees the nearest block its version has |
| A name no version has (`"grassblock"`) | an error that lists the nearest real names        |

- A block name may list `|` alternatives (`"deepslate|stone"`): the first one
  the game version knows wins. Write `"future_block|obsidian"` to pick the
  substitute yourself. Without `|`, an unknown name becomes the nearest block,
  never air.

## Writing blocks

| Call                                                         | Returns | Purpose                                                            |
| ------------------------------------------------------------ | ------- | ------------------------------------------------------------------ |
| [`world.set_block(pos, block, opts?)`](/ref/World/set_block) | —       | Sets one block, live, stored and sent                              |
| [`world.set_blocks(changes)`](/ref/World/set_blocks)         | —       | Sets many blocks at once; the cheapest way                         |
| [`world.fill(from, to, block)`](/ref/World/fill)             | —       | Fills a box between two corners, live, stored and sent to everyone |

`block` is a `BlockRef`: a name string or a custom-block handle. Both
`set_block` and `set_blocks` take `skin` for player heads — a row of
`set_blocks` is `{ at = ..., block = ..., skin = ... }`.

## Reading blocks

**A read never generates.** A position in an unloaded chunk reads as `nil`
(not loaded), not `"air"`. Inside `on_generate`, `chunk:get` always works. A
block change is stored, so late joiners see it.

| Call                                                  | Returns                   | Purpose                                                                         |
| ----------------------------------------------------- | ------------------------- | ------------------------------------------------------------------------------- |
| [`world.get_block(pos)`](/ref/World/get_block)        | `string?`                 | The block's name; `nil` where the chunk is not in memory                        |
| [`world.get_blocks(from, to)`](/ref/World/get_blocks) | `{string?}`               | A box of names, in x, then z, then y order                                      |
| [`world.block(pos)`](/ref/World/block)                | `BlockAt?`                | The block there as the handle a hook gets                                       |
| [`world.light_at(pos)`](/ref/World/light_at)          | `number, number, boolean` | Block light and sky light, 0 to 15, and whether nothing above holds off the sky |
| [`world.get_biome(pos)`](/ref/World/get_biome)        | `string?`                 | The biome name of the column; `nil` where not in memory                         |

`world.block` gives the live handle every block hook receives:

- Reads are the world as it is now; what it does lands on the next tick, like
  `world.set_block`.
- Fields read (`at`, `name` with its namespace, `room`); methods act:
  [`block:get(face)`](/ref/BlockAt/get), [`block:set(block)`](/ref/BlockAt/set),
  [`block:destroy()`](/ref/BlockAt/destroy), `block:become(entity, data)`,
  `block:drop(item, count?)`, `block:schedule()`, `block:notify()`.
- `block.state` and `block.data` are for blocks this pack defined. On any other
  block they are an error.
- A handle you keep does nothing once its block is gone.

## Player heads

A `"player_head"` or `"player_wall_head"` shows a face when you give it a
`skin`:

```luau
world.set_block(vec3(0, 65, 0), "player_head[rotation=8]", { skin = "Notch" })
world.set_block(vec3(1, 65, 0), "player_wall_head[facing=south]", { skin = player.name })
world.set_block(vec3(2, 65, 0), "player_head", { skin = { value = "ewogICJ0aW1l...", signature = "..." } })
world.set_blocks({ { at = vec3(3, 65, 0), block = "player_head", skin = "jeb_" } })
```

| Form                        | Meaning                                                      |
| --------------------------- | ------------------------------------------------------------ |
| a name string               | looked up from a player in this room, else from Mojang       |
| `{ value = , signature = }` | the account's `textures` property; the signature is optional |

- The head appears at once and gets its face later. A name with no account
  leaves a plain head and logs a line.
- The `{ value = , signature = }` form is the account's `textures` property, as
  for `world.npc{ skin = }`.
- The face is saved with the chunk. Replacing, breaking or turning the head
  forgets it: write the new state with its `skin` again.
- A head in a `.schem` (Sponge or MCEdit) or an imported world keeps its face
  through pastes, turns and `citadel import`. A head saved with only a name is
  looked up when its chunk loads.
- `skin` on any other block is an error.
- Clients from 1.7 see the face. Bedrock clients see no face.

For a head as an **item** — a face in a hand, a hotbar slot, a menu — see
[Inventory](/wiki/inventory).

## Half blocks: `detail = 2`

At `detail = 2` in [`world.build`](/ref/World/build), every coordinate is a
half block. The engine turns each block's eight cells into the block, a slab or
a stair of the material, with the correct `facing`, `half` and `shape`:

```luau
local roof = world.build(function(b)
    for k = 0, 9 do                          -- a 45-degree roof, half a block a step
        b:box(vec3(k, k, 0), vec3(19 - k, k, 15), "deepslate_tiles")
    end
end, { detail = 2 })                         -- 10 blocks wide: coordinates 0..19
```

| cells of a block                           | what is placed                                          |
| ------------------------------------------ | ------------------------------------------------------- |
| all eight                                  | the block                                               |
| the bottom four, or the top four           | a bottom or top slab                                    |
| a half and one quarter above it (or below) | an outer-corner stair                                   |
| a half and two quarters on one side        | a straight stair, climbing that side                    |
| a half and three quarters                  | an inner-corner stair                                   |
| anything else                              | the block when four or more cells hold it, else nothing |

- The slab and the stair are the material's own: `stone_bricks` makes
  `stone_brick_slab` and `stone_brick_stairs`, `oak_planks` makes `oak_slab`,
  `quartz_block` makes `quartz_stairs`.
- A material with no slab or stairs, or whose slab or stairs came in a later
  release (concrete's), is the whole block or nothing.
- Only full blocks are fitted. A lantern, flower, fence or stair named directly
  is placed as named in a block with no full-block cells. So a detail is one
  `b:block`, not eight.
- A block that holds two materials takes the one most of its cells hold.
- `detail` is `1` (the default) or `2`. `build.size` and `build.min` are in
  blocks. The cube limit counts cells, so detail 2 holds an eighth as many
  blocks.

## What a block does on its own

[`game.block(name)`](/ref/Game/block) returns one block in **this version's**
numbers, or `nil` if this game lacks it. Its `behaviour` field is the rule
Citadel runs for the block — `"grass"`, `"flowing"`, `"torch"` or `"falling"` —
or `nil` for an inert block. `resistance`, `flammability` and `material` are
`nil`, not zero, in a game with no block-update tables. Everything is
read-only. The full field table is in [Game data](/wiki/game-data).

## See also

- [Terrain generation](/wiki/terrain-generation) — chunk reads inside
  `on_generate`, biomes, and the declared world.
- [Custom blocks](/wiki/custom-blocks) — `game.blocks.define`, the block
  handle, `state` and `data`.
- [Game data](/wiki/game-data) — `game.block(name)` fields and block
  behaviour rules.
- [Building](/wiki/building) — `world.build`, where `detail = 2` fits slabs and
  stairs.
- [Client versions](/appendix/client-versions) — which clients see which
  blocks and features.
