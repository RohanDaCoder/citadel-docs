---
title: Build a cottage
section: guides
order: 1
description: Code a cottage — plinth, walls, set-back windows, gable roof, garden — as one world.build with named parts, paste it into generated ground, and check it with the citadel CLI.
tags: [tutorial, building, world.build, chunk paste, render, check]
---

# Build a cottage

> **In short:** this tutorial builds a whole cottage in code — footing, walls,
> windows, roof and garden — as one `world.build` with named parts, pastes it
> into generated terrain, and holds the sky at sunset. It is the guide for
> building well.

## What you build

- A cottage of 9 by 7 blocks on a cobblestone plinth, with oak posts and
  white walls.
- Windows set back into the wall, with a sill under each.
- A gable roof of stairs that overhangs the walls, and a brick chimney.
- A garden: a path, a fence, flowers, a tree and a barrel.

## Before you start

Read [Quick start](/wiki/quick-start) first. This guide is about building
well, and the code is simple.

## 1. Plan before code

A good build starts as a plan, not as blocks. Write it at the top of
`main.luau`:

```luau
-- main.luau
-- Plan: a small cottage, known at a glance by its steep roof and chimney.
--   footing   a cobblestone plinth, one block wider than the walls
--   body      9 by 7, white walls between oak posts, three blocks tall
--   openings  windows set back, with a sill under each; the door faces south
--   roof      a gable of stairs along x, overhanging by one; a chimney
--   setting   a path to the door, a fenced garden, a tree, a barrel
-- The middle of the door is x = 0, so the cottage is symmetric in x.
```

The plan answers four questions: what makes the build recognisable, its
parts in the order you build them, where it stands, and where the detail
goes. Keep the middle of the door at x = 0: then the house is symmetric,
and every number on the left has a partner on the right.

## 2. One build, in parts

[`world.build`](/ref/World/build) makes a build in code: a schematic with no
file. It gets a builder, `b`, with three calls: `b:block` sets one block,
`b:box` fills a box between two corners, and `b:line` draws a line.

```luau
-- main.luau
-- One build from two parts; `b:part` names each stage inside them.
local cottage = world.build(function(b)
    house(b)
    garden(b)
end)
```

The house and the garden are two modules, each a function that takes the
builder. Inside them, `b:part("walls", ...)` names what it writes. The
names show up when you check and render the build, below.

## 3. The footing

A plinth one block wider than the walls makes the house stand on something:

```luau
-- house.luau
b:part("plinth", function()
    for x = -5, 5 do
        for z = -4, 4 do
            b:block(vec3(x, 0, z), if mix(x, 0, z) < 0.3 then "mossy_cobblestone" else "cobblestone")
        end
    end
    b:box(vec3(-3, 0, -2), vec3(3, 0, 2), "spruce_planks") -- the floor inside
end)
```

A plain cobblestone floor looks flat, so one block in three is mossy. `mix`
decides which:

```luau
-- mix.luau
--!strict
-- 0..1, the same every time for the same block. A wall mixed from two
-- blocks by it builds the same way after every restart.

local function mix(x: number, y: number, z: number): number
    local v = math.sin(x * 12.9898 + y * 4.1414 + z * 78.233) * 43758.5453
    return v - math.floor(v)
end

return mix
```

`math.random` would give a new pattern on every restart. `mix` gives the
same number for the same block every time, so the wall never changes.

## Try it

Render the build at this stage (the commands are in step 9): the plinth is
one block wider than the walls, and about one block in three is mossy —
the same ones after every restart.

## 4. The walls

The walls go up in two `b:box` calls:

```luau
-- house.luau
b:part("walls", function()
    b:box(vec3(-4, 1, -3), vec3(4, 3, 3), "white_terracotta")
    b:box(vec3(-3, 1, -2), vec3(3, 3, 2), "air") -- hollow inside
    for _, x in { -4, 0, 4 } do -- oak posts at the corners and the middle
        for _, z in { -3, 3 } do
            b:box(vec3(x, 1, z), vec3(x, 3, z), "oak_log")
        end
    end
    -- The beam the roof sits on: a ring on the walls, so the room inside
    -- is open up to the roof.
    b:box(vec3(-4, 4, -3), vec3(4, 4, 3), "spruce_planks")
    b:box(vec3(-3, 4, -2), vec3(3, 4, 2), "air")
end)
```

- Fill the whole box, then hollow it out: two lines instead of four walls.
- Oak posts at the corners and in the middle of the long walls stand in
  front of the white wall. That is the timber frame.
- The beam on top is a ring, so the room inside is open up to the roof.

## 5. Windows and the door

A window is not a pane in a flat wall. It is a hole with the glass set
back, and a sill under it:

```luau
-- house.luau
b:part("openings", function()
    for _, x in { -2, 2 } do -- two windows in each long wall, a sill under each
        for _, z in { -3, 3 } do
            local out = if z < 0 then -1 else 1
            b:block(vec3(x, 2, z), "air")
            b:block(vec3(x, 2, z - out), "glass_pane") -- set back into the wall
            b:block(vec3(x, 1, z + out), `spruce_trapdoor[half=top,facing={if out > 0 then "south" else "north"}]`)
        end
    end
    for _, x in { -4, 4 } do -- one in each end wall
        local out = if x < 0 then -1 else 1
        b:block(vec3(x, 2, 0), "air")
        b:block(vec3(x - out, 2, 0), "glass_pane")
    end
    b:block(vec3(0, 1, 3), "spruce_door[facing=south,half=lower]")
    b:block(vec3(0, 2, 3), "spruce_door[facing=south,half=upper]")
    b:block(vec3(0, 3, 4), "lantern[hanging=true]") -- under the eaves
end)
```

- `out` is which way the wall faces: the glass goes one block in, the sill
  one block out.
- A block name can carry its state: `spruce_trapdoor[half=top,facing=north]`
  is a trapdoor on the top half of its block, which reads as a sill.
- The lantern hangs under the eaves, over the door.

## Try it

For every window at x = -2 there is one at x = 2, and the door sits at
x = 0: the build is symmetric in x.

## 6. The roof

The gable steps in and up from both sides, to the ridge:

```luau
-- house.luau
b:part("roof", function()
    -- Four rows of stairs a side, each one block in and one block up.
    for k = 0, 3 do
        b:box(vec3(-5, 4 + k, -4 + k), vec3(5, 4 + k, -4 + k), "spruce_stairs[facing=south]")
        b:box(vec3(-5, 4 + k, 4 - k), vec3(5, 4 + k, 4 - k), "spruce_stairs[facing=north]")
        -- The gable ends, filled under the roof.
        if k < 3 then
            for _, x in { -4, 4 } do
                b:box(vec3(x, 5 + k, -2 + k), vec3(x, 5 + k, 2 - k), "spruce_planks")
            end
        end
    end
    b:box(vec3(-5, 8, 0), vec3(5, 8, 0), "spruce_slab") -- the ridge
    b:box(vec3(3, 1, -2), vec3(3, 9, -2), "bricks") -- the chimney, through the roof
end)
```

Each row of stairs is one block in and one block up from the one below,
from both sides, until they meet at the ridge. The stairs face the middle.
The rows start one block outside the walls: the overhang throws a shadow,
and the house stops looking like a box. The chimney goes up through the
roof from the floor inside.

## 7. The garden

A build with bare grass round it floats. The garden sets the house in a
place:

```luau
-- garden.luau
b:box(vec3(0, 0, 5), vec3(0, 0, 11), "dirt_path")
for _, x in { -6, 6 } do
    b:box(vec3(x, 1, 5), vec3(x, 1, 9), "oak_fence")
end
b:box(vec3(-6, 1, 9), vec3(-2, 1, 9), "oak_fence") -- a gap for the path
b:box(vec3(2, 1, 9), vec3(6, 1, 9), "oak_fence")
```

Fences join their neighbours on their own. The gap in the front fence is
where the path goes through.

```luau
-- garden.luau
for x = -5, 5 do
    for z = 5, 8 do
        if x ~= 0 and mix(x, 1, z) < 0.35 then
            b:block(vec3(x, 1, z), if mix(z, 1, x) < 0.5 then "poppy" else "dandelion")
        end
    end
end
```

```luau
-- garden.luau
-- A tree beside the house, and a barrel by the wall.
b:box(vec3(-8, 1, -1), vec3(-8, 4, -1), "oak_log")
b:box(vec3(-10, 4, -3), vec3(-6, 5, 1), "oak_leaves")
b:box(vec3(-9, 6, -2), vec3(-7, 6, 0), "oak_leaves")
b:block(vec3(5, 1, 2), "barrel[facing=up]")
```

## 8. Into the world

The build exists; now put it in the world:

```luau
-- main.luau
world.on_generate(function(chunk)
    chunk:fill(vec3(chunk.min.x, 63, chunk.min.z), vec3(chunk.max.x, 63, chunk.max.z), "dirt")
    chunk:fill(vec3(chunk.min.x, 64, chunk.min.z), vec3(chunk.max.x, 64, chunk.max.z), "grass_block")
    -- A paste puts the build's lowest corner at the origin; adding
    -- `cottage.min` puts the build's own (0, 0, 0) at (0, 64, 0).
    chunk:paste(cottage, vec3(0, 64, 0) + cottage.min) -- only the part in this chunk
end)
```

[`chunk:paste`](/ref/Chunk/paste) puts the part of the cottage that falls in
each chunk as the chunk is made. A paste puts the build's lowest corner at
the origin; adding `cottage.min` puts the build's own `(0, 0, 0)` at
`(0, 64, 0)` instead.

```luau
-- main.luau
world.time("sunset")

players.on_join(function(player)
    player.ui.title{ title = "Home", subtitle = "a cottage built in code", color = "gold" }
end)
```

`world.time("sunset")` holds the sky at sunset: low light makes the roof
and the walls stand out.

## Try it

Run the pack and join: the middle of the door lands at `(0, 64, 0)`, the
sky stays at sunset, and the title Home shows.

## 9. Look, then fix

Build it in stages, and look at each stage before the next. On your own
machine, `citadel render` draws the build to a picture, and `citadel check`
measures it:

```sh
citadel render ./cottage --view approach,sides --out cottage.png
citadel check ./cottage --enclosed --storeys 1
```

`check` names what to fix: a room nobody can walk to, a flat wall, a
window with no depth, bare ground round the build. The first version of
this cottage had a closed ceiling that made a sealed second floor, and no
window in its end walls; the check found both.

## The whole pack

```luau
-- main.luau
--!strict
-- A cottage by a path: built in code, pasted into the ground, lit by sunset.

-- Plan: a small cottage, known at a glance by its steep roof and chimney.
--   footing   a cobblestone plinth, one block wider than the walls
--   body      9 by 7, white walls between oak posts, three blocks tall
--   openings  windows set back, with a sill under each; the door faces south
--   roof      a gable of stairs along x, overhanging by one; a chimney
--   setting   a path to the door, a fenced garden, a tree, a barrel
-- The middle of the door is x = 0, so the cottage is symmetric in x.

local house = require("house")
local garden = require("garden")

-- One build from two parts; `b:part` names each stage inside them.
local cottage = world.build(function(b)
    house(b)
    garden(b)
end)

world.on_generate(function(chunk)
    chunk:fill(vec3(chunk.min.x, 63, chunk.min.z), vec3(chunk.max.x, 63, chunk.max.z), "dirt")
    chunk:fill(vec3(chunk.min.x, 64, chunk.min.z), vec3(chunk.max.x, 64, chunk.max.z), "grass_block")
    -- A paste puts the build's lowest corner at the origin; adding
    -- `cottage.min` puts the build's own (0, 0, 0) at (0, 64, 0).
    chunk:paste(cottage, vec3(0, 64, 0) + cottage.min) -- only the part in this chunk
end)

world.time("sunset")

players.on_join(function(player)
    player.ui.title{ title = "Home", subtitle = "a cottage built in code", color = "gold" }
end)
```

```luau
-- house.luau
--!strict
-- The house: plinth, walls, openings and roof, written round (0, 0, 0),
-- the middle of the door's wall line. See main.luau for the plan.

local mix = require("mix")

return function(b)
    b:part("plinth", function()
        for x = -5, 5 do
            for z = -4, 4 do
                b:block(vec3(x, 0, z), if mix(x, 0, z) < 0.3 then "mossy_cobblestone" else "cobblestone")
            end
        end
        b:box(vec3(-3, 0, -2), vec3(3, 0, 2), "spruce_planks") -- the floor inside
    end)

    b:part("walls", function()
        b:box(vec3(-4, 1, -3), vec3(4, 3, 3), "white_terracotta")
        b:box(vec3(-3, 1, -2), vec3(3, 3, 2), "air") -- hollow inside
        for _, x in { -4, 0, 4 } do -- oak posts at the corners and the middle
            for _, z in { -3, 3 } do
                b:box(vec3(x, 1, z), vec3(x, 3, z), "oak_log")
            end
        end
        -- The beam the roof sits on: a ring on the walls, so the room inside
        -- is open up to the roof.
        b:box(vec3(-4, 4, -3), vec3(4, 4, 3), "spruce_planks")
        b:box(vec3(-3, 4, -2), vec3(3, 4, 2), "air")
    end)

    b:part("openings", function()
        for _, x in { -2, 2 } do -- two windows in each long wall, a sill under each
            for _, z in { -3, 3 } do
                local out = if z < 0 then -1 else 1
                b:block(vec3(x, 2, z), "air")
                b:block(vec3(x, 2, z - out), "glass_pane") -- set back into the wall
                b:block(vec3(x, 1, z + out), `spruce_trapdoor[half=top,facing={if out > 0 then "south" else "north"}]`)
            end
        end
        for _, x in { -4, 4 } do -- one in each end wall
            local out = if x < 0 then -1 else 1
            b:block(vec3(x, 2, 0), "air")
            b:block(vec3(x - out, 2, 0), "glass_pane")
        end
        b:block(vec3(0, 1, 3), "spruce_door[facing=south,half=lower]")
        b:block(vec3(0, 2, 3), "spruce_door[facing=south,half=upper]")
        b:block(vec3(0, 3, 4), "lantern[hanging=true]") -- under the eaves
    end)

    b:part("roof", function()
        -- Four rows of stairs a side, each one block in and one block up.
        for k = 0, 3 do
            b:box(vec3(-5, 4 + k, -4 + k), vec3(5, 4 + k, -4 + k), "spruce_stairs[facing=south]")
            b:box(vec3(-5, 4 + k, 4 - k), vec3(5, 4 + k, 4 - k), "spruce_stairs[facing=north]")
            -- The gable ends, filled under the roof.
            if k < 3 then
                for _, x in { -4, 4 } do
                    b:box(vec3(x, 5 + k, -2 + k), vec3(x, 5 + k, 2 - k), "spruce_planks")
                end
            end
        end
        b:box(vec3(-5, 8, 0), vec3(5, 8, 0), "spruce_slab") -- the ridge
        b:box(vec3(3, 1, -2), vec3(3, 9, -2), "bricks") -- the chimney, through the roof
    end)
end
```

```luau
-- garden.luau
--!strict
-- The setting: a path to the door, a fenced garden with flowers, a tree
-- and a barrel. It is what makes the house sit in a place.

local mix = require("mix")

return function(b)
    b:part("garden", function()
        b:box(vec3(0, 0, 5), vec3(0, 0, 11), "dirt_path")
        for _, x in { -6, 6 } do
            b:box(vec3(x, 1, 5), vec3(x, 1, 9), "oak_fence")
        end
        b:box(vec3(-6, 1, 9), vec3(-2, 1, 9), "oak_fence") -- a gap for the path
        b:box(vec3(2, 1, 9), vec3(6, 1, 9), "oak_fence")

        for x = -5, 5 do
            for z = 5, 8 do
                if x ~= 0 and mix(x, 1, z) < 0.35 then
                    b:block(vec3(x, 1, z), if mix(z, 1, x) < 0.5 then "poppy" else "dandelion")
                end
            end
        end

        -- A tree beside the house, and a barrel by the wall.
        b:box(vec3(-8, 1, -1), vec3(-8, 4, -1), "oak_log")
        b:box(vec3(-10, 4, -3), vec3(-6, 5, 1), "oak_leaves")
        b:box(vec3(-9, 6, -2), vec3(-7, 6, 0), "oak_leaves")
        b:block(vec3(5, 1, 2), "barrel[facing=up]")
    end)
end
```

## Where to go next

Try:

- Add a porch over the door: two posts and a small roof of slabs.
- Turn the cottage into a street: paste it three times along the path,
  and change the wall colour of each with a `mix` of the position.
- Put a bed, a table and a fireplace inside, and check that a player can
  walk to each.

Then go deeper:

- [Building](/wiki/building) — `world.build`, schematics, named parts.
- [Block reference](/wiki/block-reference) — block names and states.
- [Terrain generation](/wiki/terrain-generation) — chunks, pasting builds.
- [World state](/wiki/world-state) — `world.time` and world settings.
- [Tooling](/wiki/tooling) — the `citadel` CLI: `render`, `check`.

## See also

- [Coin rush](/wiki/guide-coin-rush) — a whole game in one pack.
- [Parkour, a room each](/wiki/guide-parkour-a-room-each) — rooms, timers,
  checkpoints.
