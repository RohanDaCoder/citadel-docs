---
title: Terrain generation
section: world
order: 1
description: Making chunks with world.on_generate and world.on_populate, the Chunk API, biomes, noise, the a0.1.0 terrain steps in citadel.yml, and declaring a whole world with world.generate rules.
tags: [terrain, chunks, on-generate, on-populate, noise, biomes, world-generate, terrain-steps]
---
# Terrain generation

> **In short:** where a chunk comes from, and everything a script can do about
> it. `world.on_generate` fills each chunk of a script world, `world.on_populate`
> adds to the engine's overworld, `noise` and biomes shape it, `terrain` in
> citadel.yml rewrites the a0.1.0 populate list, and `world.generate` declares a
> whole world as rules the engine builds on every core with no script per chunk.

## Where a chunk comes from

The `world` key in the pack's manifest says where a chunk comes from:

| `world` key | Chunks |
| --- | --- |
| `"script"` | `world.on_generate` makes them. A chunk it does not fill is air. |
| `"overworld"` | Citadel's terrain: biomes, hills, caves, ores, trees, sea level 63. Scripts only add to it (`world.on_populate`). `seed` pins the map. |
| any other name | A world folder in the pack — `<pack>/hub` for `world: hub` — made once from a build or a vanilla world. The server reads it chunk by chunk and saves player changes into it. A chunk the folder lacks comes from `world.on_generate`, or is air. |
| no key | The scripts are asked first. A chunk no script filled is overworld terrain on a `mode: full` server and air on a `mode: lite` server. |

**Chunks nobody is near are unloaded.** Every ten seconds the server drops
chunks beyond the view distance of all players and entities. When someone
returns, a stored world loads the chunk from disk (a changed chunk waits for
its save); a `script` world calls `on_generate` again. The chunks around the
spawn are generated before the port opens.

The world's `level.json` keeps the seed, spawn, time and weather of the first
run. Changing `seed` does nothing to an existing world — delete the world
folder for a new map. A reload keeps the world: a changed `world.on_generate`,
`seed` or `terrain` applies only to chunks generated from here on.

## `on_generate`

[`world.on_generate(fn: (chunk: Chunk) -> ())`](/ref/World/on_generate) is
called for a chunk each time it comes into memory, in a script world. It is a
**single-handler setter**: a later call replaces the previous handler, and it
returns nothing.

> **Gotcha:** because chunks unload and generate again, `on_generate` must make
> the same blocks every time. Draw from a hash of the position, never
> `math.random`. A script-world chunk changed live (`world.set_block`,
> `world.fill`) stays in memory.

Chunk callbacks keep their own **2 s limit**, separate from the tick budget —
and the engine waits **60 s** for a chunk; a chunk that is not ready then is
air. That wait is what lets a generator fetch data over `http` inside
`on_generate`; make the chunk without the data when the fetch fails.

## `on_populate`

[`world.on_populate(fn: (chunk: Chunk) -> ())`](/ref/World/on_populate) works on
the engine's overworld (`world: overworld`, or `mode: full` with no `world`
key). It gets each new chunk with terrain, caves and ores in place, with the
same `chunk:get`, `chunk:set` and `chunk:fill` as `on_generate`. Use it for
your own ores and trees. Like `on_generate` it is a single-handler setter, and
a changed hook reaches new land only.

## The chunk API

A chunk is a 16 by 16 column of blocks, handed to `world.on_generate`,
`world.on_populate` and a room's `generate` to fill. Fields: `chunk.x` and
`chunk.z` are the chunk coordinates (16 blocks each); `chunk.min` is the
chunk's lowest corner, inclusive (y runs 0..255 or the game version's height),
and `chunk.max` the highest, inclusive.

| Call | Returns | Purpose |
| --- | --- | --- |
| [`chunk:get(pos: Vec3)`](/ref/Chunk/get) | `string` | The block there now, by name; air outside the chunk |
| [`chunk:set(pos: Vec3, block: string)`](/ref/Chunk/set) | — | Sets one block; positions outside the chunk are ignored |
| [`chunk:fill(from: Vec3, to: Vec3, block: string)`](/ref/Chunk/fill) | — | Fills a box of blocks, clipped to the chunk |
| [`chunk:paste(schem, origin, opts?)`](/ref/Chunk/paste) | — | Pastes a build or schematic, clipped to this chunk |
| [`chunk:get_biome(pos: Vec3)`](/ref/Chunk/get_biome) | `string?` | The biome of the column at `pos`; `nil` outside the chunk |
| [`chunk:set_biome(pos: Vec3, biome: string)`](/ref/Chunk/set_biome) | — | Sets one column's biome: a vanilla name or a `game.biomes.define` name |
| [`chunk:fill_biome(from: Vec3, to: Vec3, biome: string)`](/ref/Chunk/fill_biome) | — | Sets the biome of every column in a box, clipped |

`chunk:paste` takes the same `{ air = true, part = "name" }` options as
[`world.paste`](/ref/World/paste): `part` names the paste for
`citadel render --part` and `citadel check`, and the build's own `b:part`s are
then inside it (`"house/roof"`).

> **Note:** a read never generates — a position in an unloaded chunk reads as
> `nil` (not loaded), not `"air"`. Inside `on_generate`, `chunk:get` always
> works.

## Making generation fast

Everything a chunk needs should be made once, at the top of the script, not
inside the generator:

- Make each **noise** at the top of the script, and ask for a chunk with one
  `grid` call — 256 `get` calls are slower.
- Make **builds** at the top of the script, and paste one per chunk.
  `world.schematic` inside `on_generate` reads the file again for every chunk.
- The engine calculates noise, so a generator stays inside its 100 ms.

## Noise

`noise` gives smooth random numbers for hills, caves and biome borders. The
same seed gives the same numbers every time.

| Option | Default | Meaning |
| --- | --- | --- |
| `seed` | 0 | the same seed gives the same numbers each time |
| `scale` | 64 | the size of one hill, in blocks |
| `octaves` | 1 | layers of detail, 1 to 16 |
| `lacunarity` | 2 | how many times finer each next layer is |
| `gain` | 0.5 | how many times as strong each next layer is |

A world with hills and two biomes:

```luau
local hills = noise.new { seed = 7, scale = 96, octaves = 4 }
local climate = noise.new { seed = 8, scale = 300 }

world.on_generate(function(chunk)
    local h = hills:grid(chunk.min.x, chunk.min.z, 16, 16)
    local c = climate:grid(chunk.min.x, chunk.min.z, 16, 16)
    for z = 0, 15 do
        for x = 0, 15 do
            local i = z * 16 + x + 1
            local at = chunk.min + vec3(x, 0, z)
            local top = 64 + math.floor(h[i] * 24)
            local dry = c[i] > 0
            chunk:fill(at, at + vec3(0, top - 1, 0), "stone")
            chunk:set(at + vec3(0, top, 0), dry and "sand" or "grass_block")
            chunk:set_biome(at, dry and "desert" or "forest")
        end
    end
end)
```

> **Tip:** `grid` gives up to 65 536 numbers (256 x 256), row by row: the
> number for `(x + dx, z + dz)` is at `[dz * width + dx + 1]`.

## Biomes

A biome is what the client colours a column by: the grass, the leaves, the
water, the sky and the fog. It is also the weather there. Each block column has
one biome.

- A column that nothing sets is `"plains"`.
- The engine's overworld sets the biomes of its own chunks. `on_populate` can
  read them and change them.
- A name is a vanilla biome name of any release: `"windswept_hills"` and
  `"mountains"` are the same hill. A wrong name is an error.
- A client that lacks a biome shows the nearest one it has. A 1.8 client shows
  `"cherry_grove"` as plains.

A pack makes biomes of its own. A new biome is a copy of a vanilla biome with
other colours and weather:

```luau
local crystal = game.biomes.define {
    name = "crystal",        -- becomes "mypack:crystal", which define returns
    like = "forest",         -- the vanilla biome to copy; "plains" when left out
    grass = "#7fd8c8",       -- each colour is a colour name or a color value
    leaves = "#58b7a6",
    water = "#3fd0ff",
    water_fog = "#0a4060",   -- the view under water
    sky = "#b0e8ff",
    fog = "#e0f6ff",         -- the far distance
    weather = "snow",        -- "rain" or "snow"; "none" or false for no weather
}

world.on_generate(function(chunk)
    chunk:fill_biome(chunk.min, chunk.max, crystal)
end)
```

- Define biomes at the top of the script. A client learns the biomes when it
  joins.
- Clients from 1.16.2 show a new biome. An older client and a Bedrock client
  show the `like` biome.
- A changed colour reaches a player on the next join. A biome that is new after
  the first player joined shows as its `like` until the server restarts. The
  console says so.
- A colour that is left out stays as `like` has it. `weather = "snow"` also
  makes the grass and leaves colder in colour, unless you set them.
- A biome does not make trees or blocks. The generator puts them there.

## The a0.1.0 terrain steps

`terrain` in citadel.yml sets the overworld's step list. Only
`game: a0.1.0` has one; `terrain` on a 1.8.9 world stops the server. Without
`terrain`, the world uses the original game's steps.

```yaml
game: a0.1.0
world: overworld
terrain:
  snow: true              # Alpha's snowy world: a frozen sea, snow on every open column
  steps:                  # the whole populate list, in order, in place of the jar's
    - { step: dungeons, count: 8 }
    - { step: clay, block: clay, size: 32, count: 10 }
    - { step: ore, block: coal_ore, size: 16, count: 20, below: 128 }
    - { step: ore, block: diamond_ore, size: 7, count: 4, below: 16 }   # four times the jar's
    - { step: trees, bonus: 10, big: 10 }
    - { step: patch, block: dandelion, count: 2 }
    - { step: patch, block: poppy, count: 1, chance: 2 }
    - { step: reeds, count: 10 }
    - { step: cactus, count: 1 }
    - { step: springs, fluid: water, count: 50, bound: 120, nesting: 1 }
    - { step: springs, fluid: lava, count: 20, bound: 112, nesting: 2 }
    - { step: snow }
```

| step | what it places |
| --- | --- |
| `dungeons` | `count` tries at a cobblestone room with a spawner and up to two chests |
| `clay` | `count` blobs of `block`, `size` long, into sand that starts under water |
| `ore` | `count` veins of `block`, `size` long, into stone below y `below` |
| `trees` | trees on the surface; one chunk in `bonus` gets one more, one in `big` grows big trees |
| `patch` | a patch of 64 tries at `block` — `count` times, or with `chance: n` one time in n |
| `reeds` | `count` clumps of sugar cane beside water |
| `cactus` | `count` clumps of cactus on sand |
| `springs` | `count` fluid sources in stone walls; `nesting` pushes them deeper |
| `snow` | a snow layer on every open column — in a `snow: true` world only |

> **Gotcha:** order matters — moving or removing a step changes everything
> after it. A block must be one the game can name, a size or a bound must be at
> least 1, and an unknown key stops the server. The list is stored in
> `level.json`; like `seed`, a later edit changes nothing for an existing
> world.

[`game.terrain`](/ref/Game/terrain) prints the original list — start an edit
from it. Its rows are the `step`, `block` and `count` of each step (see
[Game data](/wiki/game-data)).

## A declared world

[`world.generate(rules: GeneratorRules) → Generated`](/ref/World/generate)
declares a world as rules. The engine makes each chunk from them, on all cores,
and no script runs for a chunk. Use it for a large world; `world.on_generate`
stays for what the rules cannot say.

```luau
local hills = fields.noise { seed = 7, scale = 96, octaves = 4 }
local dry = fields.noise { seed = 8, scale = 300 }:gt(0)

local made = world.generate {
    height = 64 + hills * 24,                -- the y of the surface
    sea = 62,                                -- water fills the open air up to here
    biomes = { { "desert", when = dry }, { "forest" } },   -- the first that holds
    surface = {                              -- the first rule that holds, for each block
        { block = "stone", when = fields.slope:gt(2), depth = 4 },
        { block = "sand", biome = "desert", depth = 4 },
        { block = "grass_block" },           -- depth 1: the top block
        { block = "dirt", depth = 4 },       -- the 3 blocks below it
    },
    rock = { { block = "stone" } },          -- the body of the land
    plants = { { block = "short_grass", chance = 0.3, biome = "forest" } },
    things = { { cell = 8, { shapes = { oak }, chance = 0.4, biome = "forest" } } },
}
made:sample(hills, pos)     -- a field's value there, as the engine calculates it
made:biome_at(pos)          -- "forest"
```

### Fields

A **field** is a number at each block, written as a recipe. `fields.noise` gives
one, and maths on fields gives more: `+ - * / ^`, a minus sign, and the
methods. A number is a field too.

```luau
-- 1 on a column with water beside it: sugar cane beside water.
local w = fields.water
local beside_water = w:at(1, 0, 0):max(w:at(-1, 0, 0)):max(w:at(0, 0, 1)):max(w:at(0, 0, -1)):gt(0.5)
plants = { { block = "sugar_cane", height = 2, chance = 0.5, when = beside_water * w:lt(0.5) } }
```

- A rule asks a question with `when`: it holds where the field is above 0.5.
  `a * b` is "and", `a:max(b)` is "or", `1 - a` is "not".
- `height` cannot use `fields.height`, `slope`, `water` or `shore`: they are
  read from it.
- `biome` in a rule is a biome name. It is the same as a `when`, and faster.

### The rules

| Key | A rule | Meaning |
| --- | --- | --- |
| `biomes` | `{ "desert", when = f }` | the first that holds names the biome of the column |
| `surface` | `{ block, biome, when, depth }` | `block` for the top `depth` blocks (1) of each surface |
| `rock` | the same | the body of the land under the surface rules |
| `plants` | `{ block, chance, biome, when, ... }` | at most one plant on a column |
| `things` | `{ cell, seed, { shapes, chance, biome, when, afloat, place, y }, ... }` | at most one thing in a grid cell |
| `fluids` | `{ block, below, biome, when }` | the carved air under `below` becomes `block`; the first that holds |

`sea` fills the open air with water up to its y, and `floor` is the block at
y 0 (`"bedrock"` for a land of its own).

- A **block** is a name, or a list with a field that chooses:
  `{ "stone", "andesite", by = fields.hash(3) * 2 }`. `floor(by)` counts
  through the list.
- A **plant** is `block`, or `blocks = { lower, upper }` for a plant of two
  blocks. With `height = f` it grows: `block` repeats, and `tip` is the top
  block. `afloat = true` puts it on the water, and `sink = 1` puts it one block
  lower (ice in the top of the sea). `clear = n` keeps `n` blocks of water free
  over a plant that grows in water.
- A column tries the plant rules in order. Each rule that holds takes its
  `chance` of the column's roll, so two rules of 0.3 and 0.2 give a plant on
  half of the columns.
- A plant stays only where the game version's own rule lets it stay, for
  example cane needs water beside the block under it, at the same level. Where
  the rule fails, the column has no plant. Light is not known yet, so a rule
  about light is not checked.
- A **thing** is one of `shapes`: builds from `world.build` or
  `world.schematic`. Its `(0, 0, 0)` goes on the block above the ground. A
  thing that crosses a chunk border is complete. Nothing stands on ground that
  is under water, but `afloat = true` puts the thing on the water.
- `density = f` makes a block solid where `f` is above 0. Use it with a `solid`
  noise for caves, overhangs and land in the air. With `height` too, a block
  must pass both.
- Without `height` and `density`, the rules add to the land that the engine's
  own terrain made (`world: overworld`): surface rules do not run, plants grow
  on each column, and a thing must stand inside one chunk.
- Make the shapes and the fields at the top of the script, within the load
  limits.

### Caves

`density` carves air under the top surface. A plant or a thing goes into that
air with `place`, and `fluids` fill it:

```luau
local caves = fields.noise { seed = 3, scale = 24, octaves = 2, solid = true }
world.generate {
    height = 72 + hills * 20,
    density = 1 - caves:abs():lt(0.12) * fields.y:gt(5),   -- caves under y 5 and up
    rock = { { block = "stone" } },
    plants = {
        { block = "moss_carpet", place = "floor", chance = 0.6 },          -- moss on cave floors
        { block = "cave_vines_plant", tip = "cave_vines", height = fields.room / 3,
          place = "ceiling", chance = 0.3 },                               -- glow berries from the ceilings
        { block = "glow_lichen[{wall}=true]", place = "wall", chance = 0.1, y = { 0, 50 } },
    },
    fluids = { { block = "water", below = 30 }, { block = "lava", below = 10 } },  -- a lake, and lava under it
    things = { { cell = 6, { shapes = { stalagmite }, place = "floor", when = fields.room:gt(5) } } },
}
```

| `place` | Where | At most |
| --- | --- | --- |
| `"top"` (the default) | on the top surface, as before | one plant on a column |
| `"floor"` | the air block over each floor of a cave | one plant on each floor |
| `"ceiling"` | the air block under each ceiling, hanging down | one plant under each ceiling |
| `"wall"` | each air block of a cave with rock on a side (plants only) | one plant in each block |

- A column can cross many caves. Each floor and each ceiling of each cave is
  its own place, with its own roll.
- `y = { low, high }` keeps a rule to the blocks it starts at from `low` to
  `high`. `when`, `chance` and `y` are read at the air block the plant starts
  in, not at the rock under it.
- A plant that grows (`height`) under a ceiling hangs down: `block` is at the
  ceiling and `tip` is the lowest block. With `blocks`, the first is at the
  ceiling. A plant never grows into rock, a fluid or another plant.
- A wall plant is one block. In its name, `{wall}` is the side the rock is on
  and `{facing}` is the side away from it: `"vine[{wall}=true]"`,
  `"wall_torch[facing={facing}]"`, `"cocoa[facing={wall}]"`.
- A thing on a floor has its `(0, 0, 0)` on the air block over the floor. A
  thing under a ceiling has its `(0, 0, 0)` on the air block under the ceiling,
  so build it down from there (negative y). A grid cell holds one thing; when
  its column has several caves, the cell's roll picks one. A thing does not
  look at fluids or at the size of the cave: use `when = fields.room:gt(n)` and
  `y` to keep it in a cave it fits.
- A fluid fills only carved air, from the floor of a cave up to `below - 1`.
  The open sky over the top surface is the `sea`'s, not the fluids'. A cave
  that opens to the sea from the side is not flooded: give it a fluid rule
  under the sea level. Plants go only where the air stays air.
- `fields.room` counts the air block, the air over it and the air under it, up
  to 64. The open sky over the top surface reads 64. Read it with `at`
  anywhere; another column's room costs one `density` read for each block of
  it. `density` cannot use `fields.room`.
- `fields.depth` is measured from `height`, so it needs a `height`.
- The game version's own plant rule holds in caves too. On 1.8.9, grass and
  flowers need dirt under them, so a stone floor keeps none. Cave blocks that
  1.8.9 does not have (moss, glow lichen, hanging roots, cave vines) stay.
  `vine` keeps its 1.8.9 rule: rock on its side.

> **Gotcha:** caves need `density` or `carvers` — a rule with `place` under the
> top, or a fluid, without one of them is an error.

### The game's own caves and structures

`carvers` and `structures` run the game version's own generators over the
declared land, with the world seed:

```luau
world.generate {
    height = 64 + hills * 20,
    rock = { { block = "stone" } },
    carvers = { "caves", "ravines" },        -- the game's tunnels and ravines
    structures = { "mineshaft", "dungeon" }, -- with rails, spawners and loot
    plants = { { block = "moss_carpet", place = "floor" } },  -- in those caves
}
```

| Key | Names | Versions |
| --- | --- | --- |
| `carvers` | `"caves"` | every version |
|  | `"ravines"` | b1.8 and later |
| `structures` | `"mineshaft"`, `"dungeon"` | 1.7 to 1.12 |

- They dig and build after the land (`height`, `density`) and before the
  plants, fluids and things, so the cave rules (`place`, `fluids`) use the
  caves they dig. They need `height` or `density`: the game's own terrain
  (`world: overworld`) has its own.
- A dungeon's spawner has its mob and its chest has its loot, as in the game.
  Without the lists, the world has none of them.
- A name this version does not have is an error that names the ones it has.

## See also

- [Block reference](/wiki/block-reference) — block names, `[property=value]`
  states, version fallbacks, and how reads behave.
- [Building](/wiki/building) — `world.build` values pasted per chunk, and
  `.schem` files.
- [Game data](/wiki/game-data) — `game.terrain` and the per-version registry.
- [Server settings](/wiki/server-settings) — citadel.yml: `game`, `world_dir`,
  `seed`, and where the world lives.
- [Runtime](/wiki/runtime) — the tick budget, and the separate 2 s chunk
  callback limit.
- [Rooms and dimensions](/wiki/rooms-and-dimensions) — other worlds and their
  own `world` tables.
