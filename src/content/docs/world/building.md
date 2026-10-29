---
title: 'Building'
description: 'world.build and the Builder API, Schematic values, pasting with world.paste and chunk:paste, turning, cropping and replacing builds, .schem import, the render/check workflow, craft advice for building well, and named parts with build mode.'
---

:::note[In short]
a build a script writes is a schematic with no file — write it
with `world.build`, turn it, crop it, paste it, or read a `.schem` from the
pack. This page covers the Builder API and the Schematic value, the size
budget, `.schem` import, the `citadel render` / `citadel check` workflow, how
to build well, and named parts with their generators and build mode.
:::

## A build is a schematic with no file

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

- Coordinates are whole blocks in the build's own space, and may be negative. A
  build written around `vec3(0, 0, 0)` lands with its middle `-build.min` from
  `origin`.
- A block name this game version lacks becomes the nearest block it has.
- `chunk:paste` and `world.paste` take a build like any schematic. Make it at
  the top of the script, not inside `on_generate`.
- A build costs only what it writes. One build may write 4 096 16-block cubes
  (32 MB, sixteen million solid blocks), in a box of up to 256 million blocks.
  For more, use several builds or a `.schem`.
- Fences, walls, glass panes and iron bars join their neighbours, and stairs
  take their corners. Write `"oak_fence"`, not its `north=true` states.

## The Builder

What [`world.build`](/ref/World/build/) hands the function it is given.
Coordinates are whole blocks of the build's own and may be negative; later
writes win. `{ detail = 2 }` makes every coordinate a half block, fitted to
slabs and stairs — see [Block reference](/world/block-reference/#half-blocks-detail--2).

| Call                                           | Returns | Purpose                                                            |
| ---------------------------------------------- | ------- | ------------------------------------------------------------------ |
| [`b:block(pos, block)`](/ref/Builder/block/)    | —       | Sets one block of the build; later writes win                      |
| [`b:box(from, to, block)`](/ref/Builder/box/)   | —       | Inclusive corners, in any order, like `chunk:fill`                 |
| [`b:line(from, to, block)`](/ref/Builder/line/) | —       | Every block the straight line between the ends passes through      |
| [`b:part(name, fn)`](/ref/Builder/part/)        | —       | What `fn` writes is a named part; nested calls name `"tower/roof"` |

### Naming the parts inside a build

A build names its pieces as it writes them, and the names stay after the paste.
`citadel render` frames a part by name. `citadel check` says which part an edit
touched.

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

- A part is the box its writes reached, in whole blocks at either detail. It
  turns and flips with the build.
- A name is 1 to 64 characters without a `/`. A part inside another part is
  named by its path, `"walls/door"`.
- A name may repeat. Selecting it takes every part with that name.
- Name the parts you will talk about: the body, each tower or wing, the roof,
  the entrance. Then "make the tower taller" stays an edit to the tower.

## Schematic values

A build is a [`Schematic`](/ref/Schematic/): a box of blocks, like a `.schem`
file read once by `world.schematic`. `size` is the build's width, height and
length in blocks; `min` is the build's own lowest corner, which is the corner
`origin` puts down — zero for a file.

| Call                                                    | Returns     | Purpose                                                               |
| ------------------------------------------------------- | ----------- | --------------------------------------------------------------------- |
| [`world.paste(schem, origin, opts?)`](/ref/World/paste/) | —           | Live, stored and sent; air is skipped unless `air = true`             |
| [`schematic:rotate(degrees)`](/ref/Schematic/rotate/)    | `Schematic` | A new build turned clockwise seen from above                          |
| [`schematic:mirror(axis)`](/ref/Schematic/mirror/)       | `Schematic` | A new build flipped: `"x"` swaps east and west, `"z"` north and south |

## Turning a build

A build turns and flips as a value; the original does not change.

- A build turns about `vec3(0, 0, 0)`, so a part drawn around its middle turns
  in place. `min` reads back the new start.
- Block states turn with it: facings, log axes, fence and pane sides, stair
  corners, door hinges, rail curves, sign and banner rotation.
- `rotate` takes 90, 180 or 270. Any other value is an error.

## Cutting a build, and changing its blocks

A build somebody made by hand is a kit of pieces. `crop` takes one piece out of
it, and `replace` makes it of other blocks. Both give a new build; the original
does not change.

- The corners are in the build's own blocks, in either order. A file's lowest
  corner is `vec3(0, 0, 0)`.
- A box that reaches outside the build is cut to it. A box with none of the
  build in it is an error that says where the build runs.
- A cropped piece has no named parts. `replace` keeps them.
- `replace` takes block names with no state. A block keeps its state where the
  new block has one like it: stairs stay stairs that face the same way. Where
  it has none, the block is the plain block. `"air"` takes a block away.
- A name that is not a block is an error that names it.
- To save memory, crop the pieces while the pack loads and keep only them: a
  file nobody holds is let go.

## `.schem` files

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

- `file` is a path inside the pack folder, written with `/`. These are errors
  that name the file: a path from the root, a path that leaves the pack with
  `..`, a missing file, and a file that is not a schematic.
- Call [`world.schematic`](/ref/World/schematic/) while the pack loads and keep
  the value. Inside `on_generate`, it reads the file again for every chunk.
- `origin` is where the build's **lowest** corner goes. The build fills `origin`
  to `origin + schem.size - vec3(1, 1, 1)`.
- Air in the build is skipped, so a paste sits on the terrain. Pass
  `{ air = true }` to place the air too.
- `chunk:paste` writes only the part inside its chunk, so the call in
  `on_generate` builds the whole thing. `world.paste` writes all of it at once,
  like `world.set_blocks`.
- Sponge v2, Sponge v3 and the old MCEdit `.schematic` all load. Block
  entities (chest contents, signs) and entities do not: a chest pastes empty.
- A paste does not turn. Turn the value first with `:rotate` or `:mirror` (see
  [turning a build](#turning-a-build)). A file's schematic has them too.
- A paste keeps the exact blocks of any release Citadel knows. A newer name
  becomes the nearest block. What nothing covers becomes air, and the log names
  and counts it once per file.

## Building well

**Plan before code.** Write the plan as a comment at the top of the build:

1. What makes it recognisable at a glance? A keep is tall, square and crowned;
   a market is low and crowded.
2. Its parts, each with bounds, material and joins: footing, body, openings,
   roof, trim, props.
3. Its setting: neighbours, ground, and the way a player approaches.
4. Where detail goes: the skyline, doors, windows, corners, the roof line,
   places a player stops.

**Build in that order, and look at each stage before the next.** End each stage
with a render and a check. Name the parts as you go (`b:part`), so renders and
the check can name them.

| stage                 | what is built                                    | look with                                           | ask                                                                                                                |
| --------------------- | ------------------------------------------------ | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| 1. massing            | the footprint, the main volumes, the roof shapes | `--view sides,roof`                                 | Does the outline say what it is? Are the proportions right: towers tall enough, roof steep enough, wings in scale? |
| 2. architecture       | openings, wall depth, eaves, how parts join      | `--view approach,entrance,plan` and `citadel check` | Are windows holes with sills and frames? Does the way in read? Can a player walk to every floor?                   |
| 3. setting and detail | paths, ground, lighting, props, trim             | `--view approach,cutaway` and `citadel check`       | Does it sit in a place? Is the detail where the eye goes?                                                          |

At each stage:

- Write down the three worst problems the pictures and the check show.
- Fix those, then look again with the same views.
- Finish every fix before the next stage.
- Render again only after a change or for a new question.

**The four ways a build fails:**

- _Painted flat._ A window keeps its glass in the wall's plane, with a sill and
  a frame that stand out in front of it; glass pushed behind a wall one block
  thick sits inside the room. Give walls depth: plinths, beams, cornices.
- _Visible boxes._ Taper what grows: a tower narrows, a roof flares at its
  eaves. Break long edges. Let parts overlap and sink into each other.
- _No setting._ Add a path, a fence, a tree, a barrel, a lamp, and shape the
  ground to meet them.
- _Detail everywhere, or nowhere._ Put detail where the eye goes.

**Half blocks are the detail.** Use `detail = 2` for shapes finer than a block:
roofs, eaves, sills, steps, cornices, arches. The build turns half steps into
stairs and slabs. Name `oak_fence` or `glass_pane` and the build joins them.

**Conventions that keep a build square.**

- An axis of symmetry runs through a block's middle, so a symmetric thing is
  odd: a door 1 or 3 wide, a gate 5, a path 3. `build:mirror("x")` of one half
  gives the other.
- A block is inside a circle when `math.sqrt(dx * dx + dz * dz) <= r + 0.5`.
  The `+ 0.5` gives flat edges.
- Mix a large surface from two or three blocks of one family, chosen by a hash
  of the position. A restart then builds the same wall.
- Write a part once, round its own middle. Place it with `build:rotate` and
  `build:mirror`.

```luau
-- Helpers a pack writes for itself; nothing here is the engine's.
local function hash(x, y, z)                         -- 0..1, the same every time
    local v = math.sin(x * 12.9898 + y * 4.1414 + z * 78.233) * 43758.5453
    return v - math.floor(v)
end
local function mix(x, y, z, blocks)                  -- { "stone_bricks", "stone_bricks", "cracked_stone_bricks" }
    return blocks[math.floor(hash(x, y, z) * #blocks) + 1]
end
local function disc(b, at, r, block)                 -- 2r + 1 across, round the block `at`
    for dx = -r, r do
        for dz = -r, r do
            if math.sqrt(dx * dx + dz * dz) <= r + 0.5 then
                b:block(at + vec3(dx, 0, dz), block)
            end
        end
    end
end
local function cone(b, at, r, height, block)         -- a tower roof, widest at `at`
    for y = 0, height do
        local rr = r * (1 - y / (height + 1))
        for dx = -r, r do
            for dz = -r, r do
                if math.sqrt(dx * dx + dz * dz) <= rr + 0.5 then
                    b:block(at + vec3(dx, y, dz), block)
                end
            end
        end
    end
end
```

**Look at it, and say what you saw.** Only `citadel render` and
`citadel check` prove a build good.

- Judge only pictures taken after the last edit.
- Fix every `fix` from `citadel check`, or say it is deliberate. Weigh advice
  against the build's purpose, and say what you chose.
- After an edit to one part, run `citadel check --since` to show the other
  parts did not change.
- The pictures are flat colour. Report textures as unchecked.
- Report what you looked at, what you fixed, and what is left.

## Seeing what you built

`citadel render <pack dir> --out view.png` runs the pack with nobody joining
and draws its world.

- Each block has its real shape, in the average colour of its textures.
- With named parts, four cameras frame them from the sides (`view-1.png` looks
  north). Otherwise they circle the spawn.

Ask for the view that answers your question:

```sh
citadel render ./castle --out v.png --view approach,entrance     # does the way in read?
citadel render ./castle --out v.png --view roof --part castle/keep
citadel render ./castle --out v.png --view plan,cutaway          # the enclosed spaces, storey by storey
citadel render ./castle --out gate.png --at 0,66,30 --look 0,70,-10   # one camera, placed
```

| view       | camera                                                   | the question it answers                                                                         |
| ---------- | -------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `sides`    | four, round the build, a little above it                 | silhouette and proportion from every side                                                       |
| `approach` | a player's eye height, out from the main door            | what a player sees walking up to it                                                             |
| `entrance` | close on the main door, eye height                       | does the way in read as the way in                                                              |
| `roof`     | high up, at an angle                                     | the roof line, and where the parts meet                                                         |
| `plan`     | straight down, to scale, one per storey                  | the enclosed spaces, walls and doors of each floor                                              |
| `cutaway`  | at an angle, one per storey                              | the enclosed spaces as a player stands in them                                                  |
| `eye`      | in each named part, where a player stands, at eye height | the part as one who walks in sees it: a hall from inside, a square from its edge                |
| `night`    | as `sides`, at night                                     | the light: only blocks that give light (lanterns, lamps, glowstone, froglights) light the build |

- `--part name` frames that part and the parts inside it.
  `--from x,y,z --to x,y,z` frames a box. Without either, `--view` frames every
  named part.
- The main door is the lowest door that opens outdoors. A build with no
  `*_door` block has no `approach` or `entrance` view.
- `plan` and `cutaway` remove everything above each storey. `--cut y` removes
  everything above `y` for any view. `--night` draws any view at night, the
  placed cameras of `--at` too.
- Under a roof, a face is lit by the sky light that comes in through the
  openings and by the light blocks near it, as in the game: a room with windows
  is light, one without is dark.
- `--around x,y,z`, `--distance d`, `--height h` and `--views n` circle a point
  instead. `--size 1280x720`, `--fov 60` and `--radius r` (how far around the
  target the world is read) change the rest.
- Each file prints one JSON line on stdout:
  `{"file":..., "view":..., "eye":[x,y,z], "look":[x,y,z]}`, with `"cut"` when
  something was removed.

:::note
a picture proves shape, depth, proportion and silhouette, not
textures: every block is one flat colour. Say so when you report on how a
build looks. At night a block is lit by the light blocks within 15 blocks of
it, as in the game; a lamp outside the views' box lights nothing.
:::

## Checking what you built

`citadel check <pack dir>` measures the named build and reports what is wrong
with it:

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
- for each innermost part: its places to stand and the detail near them (blocks
  within reach that are not a full cube and not glass)
- the doors, and where each opens
- each face: how much is one plane, its windows and how many are framed, its
  materials
- the roof: how much is one height, how much is stairs and slabs
- the setting: how much of the ground around it has something placed

Then it lists the findings:

| finding          | kind                  | what it means                                                                                           |
| ---------------- | --------------------- | ------------------------------------------------------------------------------------------------------- |
| `FLOATING`       | fix                   | blocks that touch nothing standing                                                                      |
| `DOOR_BLOCKED`   | fix                   | a block in a door's way at foot or head height, named                                                   |
| `DOOR_DROP`      | fix                   | a door that opens onto nothing to stand on                                                              |
| `DOOR_UNREACHED` | fix                   | a door nobody can walk to from outside                                                                  |
| `UNREACHED`      | fix                   | floor inside walls and under a roof that nobody can walk to from outside                                |
| `STOREYS`        | fix                   | `--storeys n` asked for, and not what enclosed spaces stand on                                          |
| `NOT_CLOSED_IN`  | fix with `--enclosed` | outside air reaches the inside with doors and windows shut, and where it comes in                       |
| `FLAT_FACE`      | advice                | a face nearly all in one plane                                                                          |
| `FLUSH_WINDOWS`  | advice                | windows with nothing in front of them: no sill, lintel or post that stands out                          |
| `ONE_MATERIAL`   | advice                | a face nearly all one block                                                                             |
| `FLAT_ROOF`      | advice                | the top one flat height, not stepped                                                                    |
| `BLOCKY_ROOF`    | advice                | a sloping roof of whole blocks where stairs could be                                                    |
| `LOW_CEILING`    | advice                | a room two blocks high                                                                                  |
| `NO_SETTING`     | advice                | bare ground all round                                                                                   |
| `BARE_FACE`      | advice                | a face with few shape blocks (stairs, slabs, walls, trapdoors, lanterns): masses without detail         |
| `DARK_AT_NIGHT`  | advice                | over half of the places a player walks to is dark at night                                              |
| `SPARSE`         | advice                | a part where players walk with little detail near them: an empty hall, square or deck                   |
| `PART_OVERLAP`   | advice                | two parts (`parts.define`) overlap without one inside the other: regenerating either rewrites the other |

- A fix is wrong for any build. Weigh advice against the build's purpose: a
  market stall is open, and a tower's roof may be flat.
- A player walks on two clear cells over something solid, steps onto stairs and
  slabs, jumps one block, drops three, and climbs ladders and vines. Blocks are
  sorted by their names.
- `--json` prints one JSON object. The command exits 1 when there is something
  to fix.
- `--since` counts changed blocks by the innermost part that holds them, and
  counts the rest as `(in no part)`.

## Named parts

`parts.define` declares a part of a stored world and the generator that writes
it — for builds you edit by hand and regenerate from code:

```luau
parts.define {
    name = "tower-3",                  -- unique; a path, "downtown/tower-3", nests
    at = vec3(56, 64, 15),             -- where the build's block (0, 0, 0) lands
    detail = 1,                        -- as world.build: 1, or 2 for half blocks
    build = function(b) ... end,       -- exactly a world.build function
}
```

The rules:

- **Nothing runs on load.** `parts.define` only declares the part. A generator
  runs on request (`citadel generate`, or `/part generate` in build mode) or
  when its code changes. A server boots the stored world and runs no generator.
- Each word of a name is 1 to 64 letters, digits, `-`, `_` and `.`.
- A duplicate name is an error that names the file of the first definition.
- A part is its whole box, air included. Writing it again clears what the old
  box held outside the new box.
- `citadel render` and `citadel check` frame the `b:part`s inside a part by
  path, for example `"tower-3/roof"`.
- On a `world: script` pack, `parts.define` logs that parts need a world
  folder, and generates nothing.

### Part states

Each part is in one of four states, kept in `<world>/parts.json`:

| state        | means                                                                   | when its code changes                                    |
| ------------ | ----------------------------------------------------------------------- | -------------------------------------------------------- |
| **clean**    | the box holds exactly what its generator last wrote                     | written again, by itself                                 |
| **modified** | somebody edited blocks in it since                                      | left alone, and reported: "its code changed"             |
| **kept**     | somebody chose its blocks: they are in `parts/<name>.schem` in the pack | ignored: the generator no longer owns it                 |
| **orphaned** | its definition is gone from the pack                                    | reported: keep it, or regenerate it to remove its blocks |

```json
{
  "tower-3": {
    "state": "modified",
    "region": [
      [48, 64, 4],
      [64, 119, 26]
    ],
    "module": "city.luau",
    "generated": "sha256:…",
    "at": "2026-09-27T14:02:11Z",
    "edits": { "count": 214, "by": { "melvin": 200, "agent:claude": 14 } }
  }
}
```

**Only people and the agent make edits, never scripts.**

- An edit in build mode counts under the player's name. An agent edit counts
  under `agent:<client>`.
- Either kind makes a clean part modified.
- Blocks your script writes are not edits: `world.set_block` from a callback, a
  door it opens, a display, a ride.
- `citadel parts` and `/part` confirm the state against the `generated` hash. A
  modified part with every edit undone is clean again.

**You regenerate or keep a whole part.** Hand edits never merge into new code.

- `regenerate` clears the part and runs its generator. On an orphan, it removes
  the blocks.
- `keep` saves the blocks to `parts/<name>.schem` as Sponge v3, the format
  `world.schematic` reads. Generating a kept part pastes that file.
- `release` deletes the file and regenerates the part.

**When the code changes.** Saving a `.luau` file reloads the pack. Parts defined
**in that file** then act as the table says.

- A clean part is written again through the tick. Unchanged blocks are skipped.
- On start, files changed while the server was down count too.
- A change to a module that a part `require`s re-runs nothing.

**Nested and overlapping parts.** A block belongs to the innermost part whose
box holds it.

- Writing a parent leaves its nested parts alone.
- An edit inside a nested part counts against it, not its parent.
- Where parts overlap without nesting, an edit counts against each.
  `citadel check` warns (`PART_OVERLAP`): regenerating one rewrites the other.

### The `citadel` commands

From the command line, on the world folder:

```sh
citadel generate <pack> --part tower-3      # run one generator into the world; --parts runs every one
citadel parts <pack>                        # every part: state, region, module, edits and who; --json
citadel regenerate <pack> --part tower-3 [--yes] [--render before.png]
citadel keep <pack> --part tower-3          # its blocks become parts/tower-3.schem
citadel release <pack> --part tower-3       # a kept part goes back to its generator
```

- `generate` makes the world folder if it is missing. It writes new and clean
  parts, pastes kept parts from their files, and refuses modified parts.
- `regenerate` of a part with hand edits needs `--yes`. Without it, it writes
  nothing and says how many blocks of whose edits it would overwrite.
- `--render file.png` writes `file-before.png` and `file-after.png`.
- Stop any server running the pack first, or use `/part` in the game.
- `citadel check` and `citadel render` read the world folder with its hand
  edits. The check report has a "part states" section: states, edits, authors,
  and code changes.

### Build mode

Build mode works only on a development copy (`citadel.env` is `"development"`),
never on a live instance. A player with the `citadel.build` permission builds
by hand. Every operator has it.

```
/build                          creative and flight, and your clicks change the world; again to stop
/build wand                     the wooden axe: left click the first corner, right click the second
/build pos1, /build pos2        a corner where you stand
/build fill <block>             the selection, filled
/build replace <from> <to>      one block for another in the selection
/build copy                     the selection, held from where you stand
/build paste                    the clipboard, the same way round you as it was copied
/build rotate <90|180|270>      the clipboard, turned about where you stood
/build mirror <x|z>             the clipboard, flipped
/build undo                     your last edit, taken back
/part                           the part you look at: its state, its region, who edited it
/part <name>, /part list        one part by name; every part
/part generate <name>           run a part's generator
/part regenerate [name] [confirm]   throw its hand edits away; asks for "confirm" when there are some
/part keep [name]               its blocks become parts/<name>.schem
/part release [name]            a kept part back to its generator
/part outline                   every part's box nearby, 15 seconds: green clean, amber modified, blue kept, red orphaned
```

- Every block a builder changes, undo included, is an edit under their name.
- Outside build mode, a click on a pack server changes no blocks.
- A place puts the held item's block, facing as in the game. A pack's own block
  item places the pack's block.
- Undo is per player, 64 edits deep. One command is one edit of at most one
  million blocks.
- Rotate and mirror turn facings, axes and shapes, as `build:rotate` and
  `build:mirror` do.
- The outline is particles for the asking player only, on clients from 1.7.

## See also

- [Terrain generation](/world/terrain-generation/) — pasting builds per chunk
  inside `on_generate`, and `world.generate` for whole worlds.
- [Block reference](/world/block-reference/) — block names, states and the
  `detail = 2` cells table.
- [Custom blocks](/world/custom-blocks/) — `game.blocks.define` blocks placed in
  builds and by hand.
- [Build a cottage](/guides/guide-build-a-cottage/) — the full walkthrough of
  plan, parts, render and check.
- [Server settings](/systems/server-settings/) — `world: hub` folders,
  `citadel generate` over a range, and where the world lives.
- [Tooling](/getting-started/tooling/) — the `citadel` CLI commands at a glance.
