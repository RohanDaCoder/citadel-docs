# SOURCE: Blocks and terrain

```luau
world.on_generate(function(chunk) end)    -- called for a chunk each time it comes into memory; same blocks every time it may wait (task.wait, http.get, stores); the chunk is done when it returns
--   chunk.x, chunk.z   chunk coordinates (16 blocks each)
--   chunk.min, chunk.max   vec3 bounds of this chunk, inclusive; y runs 0 .. 255, the game version's height, for every client
--   chunk:get(pos)   what is there now, by name; air outside the chunk
--   chunk:set(pos, block)   one block; positions outside the chunk are ignored
--   chunk:fill(from, to, block)   a box, clipped to the chunk
--   chunk:paste(schem, origin)   a schematic, clipped to the chunk
--   chunk:set_biome(pos, biome)   the biome of one column; see "biomes"
--   chunk:fill_biome(from, to, biome)   the biome of each column in a box
--   chunk:get_biome(pos)   the biome name there; nil outside the chunk
world.set_block(pos, block)    -- live change, stored and sent to everyone
world.set_block(pos, "player_head[rotation=8]", { skin = "Notch" })    -- a head with a face; see "player heads"
world.set_blocks({ { at = vec3(...), block = "red_wool" }, ... })    -- many at once, cheapest; a row takes skin = too
world.fill(from, to, block)    -- live box
world.get_block(pos)    -- the block name there, or nil (see below)
world.block(pos)    -- the block there as a handle: its state, its data, whether it is powered; see "power"
world.get_blocks(from, to)    -- a box of names in one pass
world.get_biome(pos)    -- the biome name of a column, or nil (chunk not loaded)
world.time("day")    -- the sky stays there; see "the time of day"
world.time(function(s) return s * 20 end)    -- asked each tick; s is seconds since this call
world.time()    -- the time of day now, 0 .. 23999; 6000 (noon) on a lite world until something sets it
world.schematic(file)    -- a .schem file in the pack, read once
--   schem.size   vec3, the build's width, height and length in blocks
--   schem.min   vec3, the build's own lowest corner (0, 0, 0 for a file)
world.build(function(b) end, { detail = 1 })    -- the same value, written in code; detail 2 is half blocks
--   b:block(pos, block)   one block
--   b:box(from, to, block)   a box, inclusive corners, like chunk:fill
--   b:line(from, to, block)   every block the straight line passes through
--   b:part(name, function() end)   what the function writes is a named part; see "naming the parts"
world.paste(schem, origin)    -- live, like world.fill; { part = "house" } names the paste
world.container(pos)    -- a chest's stacks, or nil; see "containers"
world.drop(pos, item)    -- a stack on the ground at a block, as a broken block leaves one
world.on_populate(function(chunk) end)    -- add to the overworld's own chunks; see "populating the overworld"
```
A build that a script writes is a schematic with no file:
```luau
local road = world.build(function(b)
    b:box(vec3(-4, 0, -48), vec3(4, 0, 48), "gray_concrete")
    b:line(vec3(0, 0, -48), vec3(0, 0, 48), "white_concrete")
    b:block(vec3(0, 1, 0), "sea_lantern")     -- later writes win
end)
road.size, road.min          -- vec3(9, 2, 97) and vec3(-4, 0, -48)
world.paste(road, vec3(0, 64, 0))             -- road.min lands here
```
The rules:
- Coordinates are whole blocks in the build’s own space, and may be
negative. A build written around `vec3(0, 0, 0)` lands with its middle
`-build.min` from `origin`.
- A block name this game version lacks becomes the nearest block it has.
- `chunk:paste` and `world.paste` take a build like any schematic. Make it
at the top of the script, not inside `on_generate`.
- A build costs only what it writes. One build may write 4 096 16-block
cubes (32 MB, sixteen million solid blocks), in a box of up to 256 million
blocks. For more, use several builds or a `.schem`.
- Fences, walls, glass panes and iron bars join their neighbours, and stairs
take their corners. Write `"oak_fence"`, not its `north=true` states.
## Player heads
A `"player_head"` or `"player_wall_head"` shows a face when you give it a
`skin`:
```luau
world.set_block(vec3(0, 65, 0), "player_head[rotation=8]", { skin = "Notch" })
world.set_block(vec3(1, 65, 0), "player_wall_head[facing=south]", { skin = player.name })
world.set_block(vec3(2, 65, 0), "player_head", { skin = { value = "ewogICJ0aW1l...", signature = "..." } })
world.set_blocks({ { at = vec3(3, 65, 0), block = "player_head", skin = "jeb_" } })
```
- A name is looked up from a player in this room, else from Mojang. The
head appears at once and gets its face later. A name with no account
leaves a plain head and logs a line.
- `{ value = , signature = }` is the account’s `textures` property, as for
`world.npc{ skin = }`. The signature is optional.
- The face is saved with the chunk. Replacing, breaking or turning the head
forgets it: write the new state with its `skin` again.
- A head in a `.schem` (Sponge or MCEdit) or an imported world keeps its
face through pastes, turns and `citadel import`. A head saved with only a
name is looked up when its chunk loads.
- `skin` on any other block is an error.
- Clients from 1.7 see the face. Bedrock clients see no face.
- For a head as an item, see “head items”.
## Half blocks: detail = 2
At `detail = 2`, every coordinate is a half block. The engine turns each
block’s eight cells into the block, a slab or a stair of the material, with
the correct `facing`, `half` and `shape`:
```luau
local roof = world.build(function(b)
    for k = 0, 9 do                          -- a 45-degree roof, half a block a step
        b:box(vec3(k, k, 0), vec3(19 - k, k, 15), "deepslate_tiles")
    end
end, { detail = 2 })                         -- 10 blocks wide: coordinates 0..19
```
| cells of a block | what is placed |
| --- | --- |
| all eight | the block |
| the bottom four, or the top four | a bottom or top slab |
| a half and one quarter above it (or below) | an outer-corner stair |
| a half and two quarters on one side | a straight stair, climbing that side |
| a half and three quarters | an inner-corner stair |
| anything else | the block when four or more cells hold it, else nothing |
- The slab and the stair are the material’s own: `stone_bricks` makes
`stone_brick_slab` and `stone_brick_stairs`, `oak_planks` makes
`oak_slab`, `quartz_block` makes `quartz_stairs`.
- A material with no slab or stairs, or whose slab or stairs came in a
later release (concrete’s), is the whole block or nothing.
- Only full blocks are fitted. A lantern, flower, fence or stair named
directly is placed as named in a block with no full-block cells. So a
detail is one `b:block`, not eight.
- A block that holds two materials takes the one most of its cells hold.
- `detail` is `1` (the default) or `2`. `build.size` and `build.min` are in
blocks. The cube limit counts cells, so detail 2 holds an eighth as many
blocks.
## Turning a build
A build turns and flips as a value; the original does not change:
```luau
local window = world.build(function(b) ... end)
local east = window:rotate(90)    -- a quarter turn clockwise seen from above: north becomes east
local back = window:rotate(180)
local left = window:mirror("x")    -- east and west swap; "z" swaps north and south
```
- A build turns about `vec3(0, 0, 0)`, so a part drawn around its middle
turns in place. `min` reads back the new start.
- Block states turn with it: facings, log axes, fence and pane sides, stair
corners, door hinges, rail curves, sign and banner rotation.
- `rotate` takes 90, 180 or 270. Any other value is an error.
## Cutting a build, and changing its blocks
A build somebody made by hand is a kit of pieces. `crop` takes one piece out
of it, and `replace` makes it of other blocks. Both give a new build; the
original does not change.
```luau
local town = world.schematic("builds/town.schem")
local tower = town:crop(vec3(140, 17, 80), vec3(172, 99, 112))    -- two corners, both inside the piece
tower.min, tower.size    -- vec3(140, 17, 80) and vec3(33, 83, 33): the piece keeps its place
local blue = tower:replace { red_nether_bricks = "blue_concrete", red_wool = "blue_wool" }
world.paste(blue, vec3(0, 64, 0))    -- its lowest corner goes here, as for any build
```
- The corners are in the build’s own blocks, in either order. A file’s
lowest corner is `vec3(0, 0, 0)`.
- A box that reaches outside the build is cut to it. A box with none of the
build in it is an error that says where the build runs.
- A cropped piece has no named parts. `replace` keeps them.
- `replace` takes block names with no state. A block keeps its state where
the new block has one like it: stairs stay stairs that face the same way.
Where it has none, the block is the plain block. `"air"` takes a block
away.
- A name that is not a block is an error that names it.
- To save memory, crop the pieces while the pack loads and keep only them:
a file nobody holds is let go.
## Naming the parts
A build names its pieces as it writes them, and the names stay after the
paste. `citadel render` frames a part by name. `citadel check` says which
part an edit touched.
```luau
local house = world.build(function(b)
    b:part("walls", function()
        b:box(vec3(-5, 0, -4), vec3(5, 4, 4), "stone_bricks")
        b:part("door", function() ... end)      -- "walls/door"
    end)
    b:part("roof", function() ... end)
end, { detail = 2 })
world.paste(house, vec3(0, 64, 0), { part = "house" })   -- "house", "house/walls", "house/roof"
chunk:paste(house, vec3(0, 64, 0), { part = "house" })   -- the same from on_generate
```
- A part is the box its writes reached, in whole blocks at either detail.
It turns and flips with the build.
- A name is 1 to 64 characters without a `/`. A part inside another part is
named by its path, `"walls/door"`.
- A name may repeat. Selecting it takes every part with that name.
- Name the parts you will talk about: the body, each tower or wing, the
roof, the entrance. Then “make the tower taller” stays an edit to the
tower.
## Seeing what you built
`citadel render <pack dir> --out view.png` runs the pack with nobody joining
and draws its world.
- Each block has its real shape, in the average colour of its textures.
- With named parts, four cameras frame them from the sides (`view-1.png`
looks north). Otherwise they circle the spawn.
Ask for the view that answers your question:
```sh
citadel render ./castle --out v.png --view approach,entrance     # does the way in read?
citadel render ./castle --out v.png --view roof --part castle/keep
citadel render ./castle --out v.png --view plan,cutaway          # the enclosed spaces, storey by storey
citadel render ./castle --out gate.png --at 0,66,30 --look 0,70,-10   # one camera, placed
```
| view | camera | the question it answers |
| --- | --- | --- |
| `sides` | four, round the build, a little above it | silhouette and proportion from every side |
| `approach` | a player’s eye height, out from the main door | what a player sees walking up to it |
| `entrance` | close on the main door, eye height | does the way in read as the way in |
| `roof` | high up, at an angle | the roof line, and where the parts meet |
| `plan` | straight down, to scale, one per storey | the enclosed spaces, walls and doors of each floor |
| `cutaway` | at an angle, one per storey | the enclosed spaces as a player stands in them |
| `eye` | in each named part, where a player stands, at eye height | the part as one who walks in sees it: a hall from inside, a square from its edge |
| `night` | as `sides`, at night | the light: only blocks that give light (lanterns, lamps, glowstone, froglights) light the build |
- `--part name` frames that part and the parts inside it.
`--from x,y,z --to x,y,z` frames a box. Without either, `--view` frames
every named part.
- The main door is the lowest door that opens outdoors. A build with no
`*_door` block has no `approach` or `entrance` view.
- `plan` and `cutaway` remove everything above each storey. `--cut y`
removes everything above `y` for any view. `--night` draws any view at
night, the placed cameras of `--at` too.
- Under a roof, a face is lit by the sky light that comes in through the
openings and by the light blocks near it, as in the game: a room with
windows is light, one without is dark.
- `--around x,y,z`, `--distance d`, `--height h` and `--views n` circle a
point instead. `--size 1280x720`, `--fov 60` and `--radius r` (how far
around the target the world is read) change the rest.
- Each file prints one JSON line on stdout: `{"file":..., "view":..., "eye":[x,y,z], "look":[x,y,z]}`, with `"cut"` when something was removed.
**What a picture proves.** Shape, depth, proportion and silhouette, not
textures: every block is one flat colour. Say so when you report on how a
build looks. At night a block is lit by the light blocks within 15 blocks of
it, as in the game; a lamp outside the views’ box lights nothing.
## Checking what you built
`citadel check <pack dir>` measures the named build and reports what is
wrong with it:
```sh
citadel check ./castle                          # every named part
citadel check ./castle --part castle/keep --storeys 3 --enclosed
citadel check ./castle --save before.snap       # write the blocks down ...
citadel check ./castle --since before.snap      # ... and say what changed, part by part
```
It lists:
- the enclosed spaces (the air closed in with doors and windows shut)
- how many blocks the build holds
- the storeys
- for each innermost part: its places to stand and the detail near them
(blocks within reach that are not a full cube and not glass)
- the doors, and where each opens
- each face: how much is one plane, its windows and how many are framed,
its materials
- the roof: how much is one height, how much is stairs and slabs
- the setting: how much of the ground around it has something placed.
Then it lists the findings:
| finding | kind | what it means |
| --- | --- | --- |
| `FLOATING` | fix | blocks that touch nothing standing |
| `DOOR_BLOCKED` | fix | a block in a door’s way at foot or head height, named |
| `DOOR_DROP` | fix | a door that opens onto nothing to stand on |
| `DOOR_UNREACHED` | fix | a door nobody can walk to from outside |
| `UNREACHED` | fix | floor inside walls and under a roof that nobody can walk to from outside |
| `STOREYS` | fix | `--storeys n` asked for, and not what enclosed spaces stand on |
| `NOT_CLOSED_IN` | fix with `--enclosed` | outside air reaches the inside with doors and windows shut, and where it comes in |
| `FLAT_FACE` | advice | a face nearly all in one plane |
| `FLUSH_WINDOWS` | advice | windows with nothing in front of them: no sill, lintel or post that stands out |
| `ONE_MATERIAL` | advice | a face nearly all one block |
| `FLAT_ROOF` | advice | the top one flat height, not stepped |
| `BLOCKY_ROOF` | advice | a sloping roof of whole blocks where stairs could be |
| `LOW_CEILING` | advice | a room two blocks high |
| `NO_SETTING` | advice | bare ground all round |
| `BARE_FACE` | advice | a face with few shape blocks (stairs, slabs, walls, trapdoors, lanterns): masses without detail |
| `DARK_AT_NIGHT` | advice | over half of the places a player walks to is dark at night |
| `SPARSE` | advice | a part where players walk with little detail near them: an empty hall, square or deck |
| `PART_OVERLAP` | advice | two parts (`parts.define`) overlap without one inside the other: regenerating either rewrites the other |
- A fix is wrong for any build. Weigh advice against the build’s purpose:
a market stall is open, and a tower’s roof may be flat.
- A player walks on two clear cells over something solid, steps onto stairs
and slabs, jumps one block, drops three, and climbs ladders and vines.
Blocks are sorted by their names.
- `--json` prints one JSON object. The command exits 1 when there is
something to fix.
- `--since` counts changed blocks by the innermost part that holds them,
and counts the rest as `(in no part)`.
Ship a build too big for `chunk:set` lines as a `.schem` in the pack folder,
and paste it:
```luau
local lobby = world.schematic("builds/lobby.schem")   -- at the top, not per chunk
world.on_generate(function(chunk)
    chunk:paste(lobby, vec3(0, 64, 0))         -- origin is the build's lowest corner
end)
world.paste(lobby, vec3(100, 64, 0))           -- the same build, live
chunk:paste(lobby, vec3(0, 64, 0), { air = true })   -- both take this third argument
```
The rules:
- `file` is a path inside the pack folder, written with `/`. These are
errors that name the file: a path from the root, a path that leaves the
pack with `..`, a missing file, and a file that is not a schematic.
- Call `world.schematic` while the pack loads and keep the value. Inside
`on_generate`, it reads the file again for every chunk.
- `origin` is where the build’s **lowest** corner goes. The build fills
`origin` to `origin + schem.size - vec3(1, 1, 1)`.
- Air in the build is skipped, so a paste sits on the terrain. Pass
`{ air = true }` to place the air too.
- `chunk:paste` writes only the part inside its chunk, so the call in
`on_generate` builds the whole thing. `world.paste` writes all of it at
once, like `world.set_blocks`.
- Sponge v2, Sponge v3 and the old MCEdit `.schematic` all load. Block
entities (chest contents, signs) and entities do not: a chest pastes
empty.
- A paste does not turn. Turn the value first with `:rotate` or `:mirror`
(see “turning a build”). A file’s schematic has them too.
- A paste keeps the exact blocks of any release Citadel knows. A newer
name becomes the nearest block. What nothing covers becomes air, and the
log names and counts it once per file.
## The time of day
The time is in ticks, 0 at dawn and 24000 to a day. Each room has its own
time, and late joiners get the same sky.
```luau
world.time("night")          -- sets the hour: sunrise 23000, day 1000, noon 6000, sunset 12000, night 13000, midnight 18000
world.time(18000)            -- sets the hour, in ticks
world.time(function(s)       -- a cycle: asked each tick, s seconds after this call
    return 1000 + s * 40     -- a day of ten minutes, from morning
end)
world.time(function(s)       -- anything the pack likes: a day that stops at dusk
    return math.min(1000 + s * 20, 12000)
end)
local now = world.time()     -- 0 .. 23999
```
- A call replaces the previous one, a function too.
- The function returns ticks or a name. If it errors, the sky stays where
it was.
- Whether the sun moves is a rule: `world.rules{ day_cycle = true }` runs
the version’s own day (20 minutes), and nothing else of survival.
- On a `mode: lite` world and in a room made by `rooms.create`, the rule is
off and the sun stays straight overhead (noon).
- On a `mode: full` world, and after `world.rules{ survival = true }`, the
rule is on.
- A number or a name sets the hour. With `day_cycle` on, the day runs on
from there, as `/time set` does. With it off, the sky stays there.
- A function drives the sky itself. The engine’s day stands aside until the
next `world.time` call.
- A stopped sky, the normal day or an `s * 20` day costs one packet a second. A faster or
slower day costs one packet every tick it moves.
Reading blocks:
```luau
local here = world.get_block(player.at - vec3(0, 1, 0))    -- "grass_block"
local box = world.get_blocks(vec3(0, 64, 0), vec3(15, 64, 15))    -- 256 names the order is x, then z, then y: index ((dx * zn) + dz) * yn + dy + 1
```
**A read never generates.** A position in an unloaded chunk reads as `nil`
(not loaded), not `"air"`. Inside `on_generate`, `chunk:get` always works.
A block change is stored, so late joiners see it. A block name may list `|`
alternatives (`"deepslate|stone"`): the first one the game version knows
wins. Without `|`, an unknown name becomes the nearest block, never air.
## Containers
A chest’s stacks, for a pipe, a quarry or a sorting machine to take from
and put into:
```luau
local box = world.container(pos)    -- nil unless the block there is a chest
box.size    -- 27
box:items()    -- { { slot = 1, item = "cobblestone", count = 12 }, ... }, the filled slots
box:take("cobblestone", 16)    -- up to 16, slot by slot; answers how many it took
box:put{ item = "brick", id = "copper_ingot", count = 5 }    -- answers how many did not fit, 0 for all of it
```
- A chest a player has open belongs to that player until they close it.
Until then, `take` and `put` do nothing.
- Each half of a double chest is its own 27 slots.
- A kept handle never goes stale. `items()` on a chest that is gone returns
an empty list.
## Populating the overworld
```luau
world.on_populate(function(chunk) end)    -- once per chunk the overworld terrain made, after it made it
```
`on_populate` works on the engine’s overworld (`world: overworld`, or
`mode: full` with no `world` key). It gets each new chunk with terrain,
caves and ores in place, with the same `chunk:get`, `chunk:set` and
`chunk:fill` as `on_generate`. Use it for your own ores and trees. A changed
hook reaches new land only.
## Biomes
A biome is what the client colours a column by: the grass, the leaves, the
water, the sky and the fog. It is also the weather there. Each block column
has one biome.
```luau
chunk:set_biome(pos, "desert")    -- one column; pos.y is not read
chunk:fill_biome(chunk.min, chunk.max, "jungle")    -- each column of a box, clipped to the chunk
chunk:get_biome(pos)    -- "jungle"; nil outside the chunk
world.get_biome(pos)    -- the same for a loaded chunk; nil when it is not loaded
```
- A column that nothing sets is `"plains"`.
- The engine’s overworld sets the biomes of its own chunks. `on_populate`
can read them and change them.
- A name is a vanilla biome name of any release: `"windswept_hills"` and
`"mountains"` are the same hill. A wrong name is an error.
- A client that lacks a biome shows the nearest one it has. A 1.8 client
shows `"cherry_grove"` as plains.
A pack makes biomes of its own. A new biome is a copy of a vanilla biome
with other colours and weather:
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
- Define biomes at the top of the script. A client learns the biomes when
it joins.
- Clients from 1.16.2 show a new biome. An older client and a Bedrock
client show the `like` biome.
- A changed colour reaches a player on the next join. A biome that is
new after the first player joined shows as its `like` until the server
restarts. The console says so.
- A colour that is left out stays as `like` has it. `weather = "snow"`
also makes the grass and leaves colder in colour, unless you set them.
- A biome does not make trees or blocks. The generator puts them there.
## Noise
`noise` gives smooth random numbers for hills, caves and biome borders. The
engine calculates them, so a generator stays inside its 100 ms.
```luau
local hills = noise.new { seed = 7, scale = 96, octaves = 4 }
hills:get(x, z)    -- about -1 .. 1, for a height
hills:get(x, y, z)    -- the same in 3D, for caves and overhangs
hills:grid(x, z, 16, 16)    -- 256 heights in one call: [dz * 16 + dx + 1]
```
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
- Make each noise at the top of the script, not inside `on_generate`.
- Ask for a chunk with one `grid` call. 256 `get` calls are slower.
- `grid` gives up to 65 536 numbers (256 x 256).
## A declared world
`world.generate` declares a world as rules. The engine makes each chunk from
them, on all cores, and no script runs for a chunk. Use it for a large world.
`world.on_generate` stays for what the rules cannot say.
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
**A field** is a number at each block, written as a recipe. `fields.noise`
gives one, and maths on fields gives more: `+ - * / ^`, a minus sign, and
the methods. A number is a field too.
```luau
fields.noise { seed = 7, scale = 96, octaves = 4, solid = false }    -- about -1 .. 1; solid = true changes with y
fields.x, fields.y, fields.z    -- the block's own coordinates
fields.height, fields.slope    -- the surface y of the column; the step to its steepest neighbour
fields.water, fields.shore    -- the water depth over the surface (0 or less on land); 1 at the water's edge
fields.depth    -- blocks under the surface: fields.height - fields.y
fields.room    -- the height of the open space the block is in (0 in rock, 64 at most)
fields.hash(cell, seed)    -- one number 0 .. 1 for each square of `cell` blocks
fields.cells(size, seed)    -- { distance = field, random = field }: the nearest point of a scattered grid
fields.mix(a, b, t)    -- a where t is 0, b where t is 1
f:abs() f:floor() f:sqrt() f:min(g) f:max(g) f:clamp(low, high)
f:gt(g) f:lt(g)    -- 1 or 0
f:smooth(from, to)    -- 0 at from, 1 at to, smooth between
f:curve({ { -1, -40 }, { 0, 2 }, { 1, 20 } })    -- straight lines through the points
f:at(dx, dy, dz)    -- f at the block that far away
```
```luau
-- 1 on a column with water beside it: sugar cane beside water.
local w = fields.water
local beside_water = w:at(1, 0, 0):max(w:at(-1, 0, 0)):max(w:at(0, 0, 1)):max(w:at(0, 0, -1)):gt(0.5)
plants = { { block = "sugar_cane", height = 2, chance = 0.5, when = beside_water * w:lt(0.5) } }
```
- A rule asks a question with `when`: it holds where the field is above
0.5. `a * b` is “and”, `a:max(b)` is “or”, `1 - a` is “not”.
- `height` cannot use `fields.height`, `slope`, `water` or `shore`: they
are read from it.
- `biome` in a rule is a biome name. It is the same as a `when`, and faster.
**The rules:**
| Key | A rule | Meaning |
| --- | --- | --- |
| `biomes` | `{ "desert", when = f }` | the first that holds names the biome of the column |
| `surface` | `{ block, biome, when, depth }` | `block` for the top `depth` blocks (1) of each surface |
| `rock` | the same | the body of the land under the surface rules |
| `plants` | `{ block, chance, biome, when, ... }` | at most one plant on a column |
| `things` | `{ cell, seed, { shapes, chance, biome, when, afloat, place, y }, ... }` | at most one thing in a grid cell |
| `fluids` | `{ block, below, biome, when }` | the carved air under `below` becomes `block`; the first that holds |
- A **block** is a name, or a list with a field that chooses:
`{ "stone", "andesite", by = fields.hash(3) * 2 }`. `floor(by)` counts
through the list.
- A **plant** is `block`, or `blocks = { lower, upper }` for a plant of two
blocks. With `height = f` it grows: `block` repeats, and `tip` is the top
block. `afloat = true` puts it on the water, and `sink = 1` puts it one
block lower (ice in the top of the sea). `clear = n` keeps `n` blocks of
water free over a plant that grows in water.
- A column tries the plant rules in order. Each rule that holds takes its
`chance` of the column’s roll, so two rules of 0.3 and 0.2 give a plant
on half of the columns.
- A plant stays only where the game version’s own rule lets it stay, for
example cane needs water beside the block under it, at the same level.
Where the rule fails, the column has no plant. Light is not known yet,
so a rule about light is not checked.
- A **thing** is one of `shapes`: builds from `world.build` or
`world.schematic`. Its `(0, 0, 0)` goes on the block above the ground. A
thing that crosses a chunk border is complete. Nothing stands on ground
that is under water, but `afloat = true` puts the thing on the water.
- `density = f` makes a block solid where `f` is above 0. Use it with a
`solid` noise for caves, overhangs and land in the air. With `height`
too, a block must pass both.
- Without `height` and `density`, the rules add to the land that the
engine’s own terrain made (`world: overworld`): surface rules do not
run, plants grow on each column, and a thing must stand inside one chunk.
- Make the shapes and the fields at the top of the script, within the load
limits (see “loading”).
**Caves.** `density` carves air under the top surface. A plant or a thing
goes into that air with `place`, and `fluids` fill it:
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
- A column can cross many caves. Each floor and each ceiling of each cave
is its own place, with its own roll.
- `y = { low, high }` keeps a rule to the blocks it starts at from `low` to
`high`. `when`, `chance` and `y` are read at the air block the plant
starts in, not at the rock under it.
- A plant that grows (`height`) under a ceiling hangs down: `block` is at
the ceiling and `tip` is the lowest block. With `blocks`, the first is at
the ceiling. A plant never grows into rock, a fluid or another plant.
- A wall plant is one block. In its name, `{wall}` is the side the rock is
on and `{facing}` is the side away from it: `"vine[{wall}=true]"`,
`"wall_torch[facing={facing}]"`, `"cocoa[facing={wall}]"`.
- A thing on a floor has its `(0, 0, 0)` on the air block over the floor. A
thing under a ceiling has its `(0, 0, 0)` on the air block under the
ceiling, so build it down from there (negative y). A grid cell holds one
thing; when its column has several caves, the cell’s roll picks one. A
thing does not look at fluids or at the size of the cave: use
`when = fields.room:gt(n)` and `y` to keep it in a cave it fits.
- A fluid fills only carved air, from the floor of a cave up to `below - 1`.
The open sky over the top surface is the `sea`’s, not the fluids’. A cave
that opens to the sea from the side is not flooded: give it a fluid rule
under the sea level. Plants go only where the air stays air.
- `fields.room` counts the air block, the air over it and the air under
it, up to 64. The open sky over the top surface reads 64. Read it with
`at` anywhere; another column’s room costs one `density` read for each
block of it. `density` cannot use `fields.room`.
- `fields.depth` is measured from `height`, so it needs a `height`.
- The game version’s own plant rule holds in caves too. On 1.8.9, grass and
flowers need dirt under them, so a stone floor keeps none. Cave blocks
that 1.8.9 does not have (moss, glow lichen, hanging roots, cave vines)
stay. `vine` keeps its 1.8.9 rule: rock on its side.
- Caves need `density` or `carvers`: a rule with `place` under the top, or
a fluid, without one of them is an error.
**The game’s own caves and structures.** `carvers` and `structures` run the
game version’s own generators over the declared land, with the world seed:
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
caves they dig. They need `height` or `density`: the game’s own terrain
(`world: overworld`) has its own.
- A dungeon’s spawner has its mob and its chest has its loot, as in the
game. Without the lists, the world has none of them.
- A name this version does not have is an error that names the ones it has.
