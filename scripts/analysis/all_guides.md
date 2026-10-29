

===== GUIDE: a-dungeon-dimension | A dungeon dimension =====

## What you build
- A castle yard of stone bricks with a square of blue carpet in it.
- `dungeon`, a second world: bedrock at both ends, mossy walls, two
crossing corridors. A client draws it with the Nether’s dark sky.
- Step on the carpet and you arrive in the dungeon. `/leave` brings you
back.
This guide builds on **Your first pack**: `world.on_generate` and
`commands.add`.
## 1. Declare the dimension
A pack adds a world in `citadel.yml`, under `dimensions:`. The name is its
id inside the pack, so this one is `castle:dungeon`:
```yaml
# citadel.yml
name: castle
entry: main.luau
motd: A castle with a dungeon under it
spawn_point: [0.5, 65.0, 0.5]
gamemode: 2
mode: lite
world: script
dimensions:
  dungeon:
    type: { has_skylight: false, has_ceiling: true, weather: false }
    world: script
```
- `type` says how the world behaves. Every field is optional and starts
from the main world’s: `has_skylight`, `has_ceiling`, `weather`,
`ultrawarm`, `bed_works`, `respawn_anchor_works`, `coordinate_scale`,
`fixed_time` and `effects`.
- A world with a roof looks like the Nether to a client, one with no sky
and no roof like the End. `effects` chooses one of the three yourself.
- `world: script` means the pack makes its chunks. `void` leaves them
empty.
The dungeon is a world of the server’s group: it ticks after the main world
and, on a server that keeps its world, saves to `world_dungeon` beside it.
## 2. The yard
The main world, as in the first guide:
```luau
-- main.luau
-- The castle yard: a stone floor, and a square of blue carpet in the middle.
world.on_generate(function(chunk)
    chunk:fill(vec3(chunk.min.x, 64, chunk.min.z), vec3(chunk.max.x, 64, chunk.max.z), "stone_bricks")
    chunk:fill(vec3(4, 65, 4), vec3(5, 65, 5), "light_blue_carpet")
end)
```
## 3. The dungeon’s terrain
`world.dimension(name)` is that world’s own `world` table. Its
`on_generate` fills the dungeon’s chunks:
```luau
-- main.luau
-- The dungeon: bedrock below and above, dark corridors in between.
local dungeon = world.dimension("dungeon")
dungeon.on_generate(function(chunk)
    chunk:fill(vec3(chunk.min.x, 63, chunk.min.z), vec3(chunk.max.x, 63, chunk.max.z), "bedrock")
    chunk:fill(vec3(chunk.min.x, 64, chunk.min.z), vec3(chunk.max.x, 68, chunk.max.z), "mossy_cobblestone")
    chunk:fill(vec3(chunk.min.x, 64, chunk.min.z + 6), vec3(chunk.max.x, 66, chunk.min.z + 9), "air")
    chunk:fill(vec3(chunk.min.x + 6, 64, chunk.min.z), vec3(chunk.min.x + 9, 66, chunk.max.z), "air")
    chunk:fill(vec3(chunk.min.x, 69, chunk.min.z), vec3(chunk.max.x, 69, chunk.max.z), "bedrock")
end)
```
## 4. The gate
A route is how a player gets from one world to another. This one starts in
the overworld, and the trigger is standing in a block:
```luau
-- main.luau
-- Step on the carpet and you are in the dungeon.
routes.add{
    from = "overworld",
    to = "dungeon",
    trigger = { block = "light_blue_carpet" },
    placement = { x = 7.5, y = 64, z = 7.5 },
}
```
- `trigger = { block = "light_blue_carpet" }` fires on the first tick a
player stands in carpet. `ticks = 80` would make them wait, as a Nether
portal does.
- `placement` is where they arrive. Leave it out and they arrive at the
dungeon’s spawn.
- After a trip a player must step out of the trigger block for half a second
before it can fire again.
## 5. The way back
`player:travel(dimension, pos)` sends a player to any world of the group, at
`pos` or, without it, at its spawn:
```luau
-- main.luau
-- `/leave` goes back up, to the yard's spawn.
commands.add("leave", function(player)
    player:travel("overworld")
end)
```
## Try it
Run the pack, step on the carpet, look up at the roof, and type `/leave`.


===== GUIDE: build-a-cottage | Build a cottage =====

## What you build
- A cottage of 9 by 7 blocks on a cobblestone plinth, with oak posts and
white walls.
- Windows set back into the wall, with a sill under each.
- A gable roof of stairs that overhangs the walls, and a brick chimney.
- A garden: a path, a fence, flowers, a tree and a barrel.
Read **Your first pack** first. This guide is about building well, and
the code is simple.
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
`world.build` makes a build in code: a schematic with no file. It gets a
builder, `b`, with three calls: `b:block` sets one block, `b:box` fills a
box between two corners, and `b:line` draws a line.
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
A plinth one block wider than the walls makes the house stand on
something. A plain cobblestone floor looks flat, so one block in three is
mossy. `mix` decides which:
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
## 4. The walls
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
## 6. The roof
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
`chunk:paste` puts the part of the cottage that falls in each chunk as
the chunk is made. A paste puts the build’s lowest corner at the origin;
adding `cottage.min` puts the build’s own `(0, 0, 0)` at `(0, 64, 0)`
instead.
```luau
-- main.luau
world.time("sunset")

players.on_join(function(player)
    player.ui.title{ title = "Home", subtitle = "a cottage built in code", color = "gold" }
end)
```
`world.time("sunset")` holds the sky at sunset: low light makes the roof
and the walls stand out.
## 9. Look, then fix
Build it in stages, and look at each stage before the next. On your own
machine, `citadel render` draws the build to a picture, and `citadel check` measures it:
```
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
## Try this next
- Add a porch over the door: two posts and a small roof of slabs.
- Turn the cottage into a street: paste it three times along the path,
and change the wall colour of each with a `mix` of the position.
- Put a bed, a table and a fireplace inside, and check that a player can
walk to each.


===== GUIDE: coin-rush | Coin rush =====

## What you build
- A round grass arena with a fence on its rim.
- Five gold pressure plates, the coins, at random places on the floor.
Walk onto one to take it; a new one appears somewhere else.
- A boss bar that counts down the round, and a sidebar with every
player’s score.
- At the end: the winner’s name on screen, fireworks, and a message to
each player who beat their best.
Read **Your first pack** first: this guide uses what it explains.
## 1. The pack
Three Luau files this time. `main.luau` runs the game, and it loads two
modules: `arena.luau` for the ground, `coins.luau` for the coins.
```yaml
# citadel.yml
name: coins
entry: main.luau
motd: Coin rush
spawn_point: [0.5, 65.0, 0.5]
gamemode: 2
mode: lite
world: script
```
## 2. The arena
A module is a file that returns a table. `require("arena")` runs
`arena.luau` once and hands back what it returned, so every file that
requires it shares one arena.
```luau
-- arena.luau
world.on_generate(function(chunk)
    for x = chunk.min.x, chunk.max.x do
        for z = chunk.min.z, chunk.max.z do
            local d = math.sqrt(x * x + z * z)
            if d <= arena.RADIUS then
                chunk:set(vec3(x, 64, z), "grass_block")
            elseif d <= arena.RADIUS + 1.5 then
                chunk:set(vec3(x, 64, z), "stone_bricks")
                chunk:set(vec3(x, 65, z), "oak_fence")
            end
        end
    end
end)
```
`math.sqrt(x * x + z * z)` is the distance from the middle. Inside the
radius is grass; a ring just outside it gets a stone floor and a fence.
Fences join their neighbours on their own: write `"oak_fence"`, and the
ring closes.
The coins need random places on the floor, away from the fence:
```luau
-- arena.luau
-- A random block on the floor, two blocks in from the fence.
function arena.spot(): vector
    local r = arena.RADIUS - 2
    while true do
        local x, z = math.random(-r, r), math.random(-r, r)
        if x * x + z * z <= r * r then
            return vec3(x, 65, z)
        end
    end
end
```
It picks a random square around the middle, and tries again until the
spot is inside the circle.
## 3. The coins
A coin is two things: a gold pressure plate that players see, and a
**zone** that notices a player walking onto it.
```luau
-- coins.luau
function coins.place(on_take: (player: any) -> ())
    -- Pick again when that spot already holds a coin.
    local at = arena.spot()
    while world.get_block(at) ~= "air" do
        at = arena.spot()
    end
    world.set_block(at, "light_weighted_pressure_plate")
    local coin = { at = at }
    -- A zone notices the player who walks onto the plate.
    coin.zone = world.zone{
        from = at,
        to = at,
        on_enter = function(player)
            coins.remove(coin)
            fx.particle("totem_of_undying", at + vec3(0.5, 0.5, 0.5), { count = 12, spread = 0.4, speed = 0.3 })
            sound.play("entity.experience_orb.pickup", { at = at, pitch = 1.2 })
            on_take(player)
        end,
    }
    table.insert(placed, coin)
end
```
- A spot that already has a coin is not `"air"`, so `place` picks again.
- `world.zone` is a box of blocks. Here it is one block, and `on_enter`
runs when a player’s feet enter it.
- Taking a coin removes it, plays a sound and a burst of particles at
it, and calls `on_take`: the game decides what a coin is worth, not the
coin.
Removing a coin puts the floor back and forgets the zone:
```luau
-- coins.luau
function coins.remove(coin)
    coin.zone:destroy()
    world.set_block(coin.at, "air")
    table.remove(placed, table.find(placed, coin) :: number)
end

function coins.clear()
    while #placed > 0 do
        coins.remove(placed[1])
    end
end
```
## 4. Scores
Each player carries their own score in `player.data`, a table that lives
as long as the player is connected. The sidebar shows everyone’s:
```luau
-- main.luau
-- The sidebar lists every player, most coins first.
local function show_scores()
    local list = players.list()
    table.sort(list, function(a, b)
        return a.data.coins > b.data.coins
    end)
    local lines = {}
    for _, p in list do
        table.insert(lines, `{p.name}  {p.data.coins}`)
    end
    ui.sidebar{ title = "COIN RUSH", lines = lines }
end

-- One coin taken: count it, and put a new one down.
local function take(player)
    player.data.coins += 1
    show_scores()
    coins.place(take)
end
```
`take` counts the coin and places a new one, so there are always five on
the floor. It passes itself to `coins.place`: the new coin calls `take`
again when someone walks onto it.
When a player joins, their score starts at 0, and `storage` tells them
their best:
```luau
-- main.luau
players.on_join(function(player)
    player.data.coins = 0
    local best = storage.get("best." .. player.uuid) or 0
    player:message(`Walk onto the gold plates! Your best is {best}.`, "gold")
    show_scores()
end)
```
`storage` keeps values across restarts. The key uses `player.uuid`, not
the name: a player can change their name, never their id.
## 5. A round
One round sends everyone to the middle, puts five coins down, and counts
down sixty seconds on a boss bar:
```luau
-- main.luau
local bar = ui.bossbar{ title = "Coin rush", color = "yellow", progress = 1 }

local function round()
    for _, p in players.list() do
        p.data.coins = 0
        p:teleport(arena.CENTER)
    end
    show_scores()
    for _ = 1, ON_FIELD do
        coins.place(take)
    end
    ui.title{ title = "GO!", color = "gold", stay = 1 }

    for left = ROUND, 1, -1 do
        bar.title = `Coin rush · {left} s`
        bar.progress = left / ROUND
        task.wait(1)
    end
    coins.clear()
    local function coins_text(n: number): string
        return if n == 1 then "1 coin" else `{n} coins`
    end
    local winner, most = nil, -1
    for _, p in players.list() do
        local key = "best." .. p.uuid
        if p.data.coins > (storage.get(key) or 0) then
            storage.set(key, p.data.coins)
            p:message(`New best: {coins_text(p.data.coins)}!`, "gold")
        end
        if p.data.coins > most then
            winner, most = p, p.data.coins
        end
    end
    if winner then
        ui.title{ title = `{winner.name} wins`, subtitle = coins_text(most), color = "gold" }
        fx.particle("firework", arena.CENTER + vec3(0, 2, 0), { count = 60, spread = 2, speed = 0.1 })
    end
end
```
`task.wait(1)` inside the loop pauses the round, not the server: coins
are taken, sounds play and other players join while it waits.
At the end the round finds the winner and saves each best score:
```luau
-- main.luau
local function coins_text(n: number): string
    return if n == 1 then "1 coin" else `{n} coins`
end
local winner, most = nil, -1
for _, p in players.list() do
    local key = "best." .. p.uuid
    if p.data.coins > (storage.get(key) or 0) then
        storage.set(key, p.data.coins)
        p:message(`New best: {coins_text(p.data.coins)}!`, "gold")
    end
    if p.data.coins > most then
        winner, most = p, p.data.coins
    end
end
if winner then
    ui.title{ title = `{winner.name} wins`, subtitle = coins_text(most), color = "gold" }
    fx.particle("firework", arena.CENTER + vec3(0, 2, 0), { count = 60, spread = 2, speed = 0.1 })
end
```
## 6. Rounds forever
```luau
-- main.luau
-- Rounds run forever: a round, a five-second break, the next round.
task.spawn(function()
    while true do
        if players.count() == 0 then
            task.wait(1)
        else
            round()
            task.wait(5)
        end
    end
end)
```
`task.spawn` runs the loop as its own script, so `main.luau` finishes
loading while the rounds go on. With nobody online it waits; otherwise
it plays a round, rests five seconds, and plays the next.
## The whole pack
```luau
-- main.luau
--!strict
-- Coin rush: sixty seconds to pick up as many coins as you can.

local arena = require("arena")
local coins = require("coins")

local ROUND = 60 -- seconds
local ON_FIELD = 5 -- coins on the floor at once

-- The sidebar lists every player, most coins first.
local function show_scores()
    local list = players.list()
    table.sort(list, function(a, b)
        return a.data.coins > b.data.coins
    end)
    local lines = {}
    for _, p in list do
        table.insert(lines, `{p.name}  {p.data.coins}`)
    end
    ui.sidebar{ title = "COIN RUSH", lines = lines }
end

-- One coin taken: count it, and put a new one down.
local function take(player)
    player.data.coins += 1
    show_scores()
    coins.place(take)
end

players.on_join(function(player)
    player.data.coins = 0
    local best = storage.get("best." .. player.uuid) or 0
    player:message(`Walk onto the gold plates! Your best is {best}.`, "gold")
    show_scores()
end)

local bar = ui.bossbar{ title = "Coin rush", color = "yellow", progress = 1 }

local function round()
    for _, p in players.list() do
        p.data.coins = 0
        p:teleport(arena.CENTER)
    end
    show_scores()
    for _ = 1, ON_FIELD do
        coins.place(take)
    end
    ui.title{ title = "GO!", color = "gold", stay = 1 }

    for left = ROUND, 1, -1 do
        bar.title = `Coin rush · {left} s`
        bar.progress = left / ROUND
        task.wait(1)
    end
    coins.clear()
    local function coins_text(n: number): string
        return if n == 1 then "1 coin" else `{n} coins`
    end
    local winner, most = nil, -1
    for _, p in players.list() do
        local key = "best." .. p.uuid
        if p.data.coins > (storage.get(key) or 0) then
            storage.set(key, p.data.coins)
            p:message(`New best: {coins_text(p.data.coins)}!`, "gold")
        end
        if p.data.coins > most then
            winner, most = p, p.data.coins
        end
    end
    if winner then
        ui.title{ title = `{winner.name} wins`, subtitle = coins_text(most), color = "gold" }
        fx.particle("firework", arena.CENTER + vec3(0, 2, 0), { count = 60, spread = 2, speed = 0.1 })
    end
end

-- Rounds run forever: a round, a five-second break, the next round.
task.spawn(function()
    while true do
        if players.count() == 0 then
            task.wait(1)
        else
            round()
            task.wait(5)
        end
    end
end)
```
```luau
-- coins.luau
--!strict
-- Coins: gold pressure plates on the floor. Walk onto one to take it.

local arena = require("arena")

local coins = {}
local placed: { any } = {}

function coins.place(on_take: (player: any) -> ())
    -- Pick again when that spot already holds a coin.
    local at = arena.spot()
    while world.get_block(at) ~= "air" do
        at = arena.spot()
    end
    world.set_block(at, "light_weighted_pressure_plate")
    local coin = { at = at }
    -- A zone notices the player who walks onto the plate.
    coin.zone = world.zone{
        from = at,
        to = at,
        on_enter = function(player)
            coins.remove(coin)
            fx.particle("totem_of_undying", at + vec3(0.5, 0.5, 0.5), { count = 12, spread = 0.4, speed = 0.3 })
            sound.play("entity.experience_orb.pickup", { at = at, pitch = 1.2 })
            on_take(player)
        end,
    }
    table.insert(placed, coin)
end

function coins.remove(coin)
    coin.zone:destroy()
    world.set_block(coin.at, "air")
    table.remove(placed, table.find(placed, coin) :: number)
end

function coins.clear()
    while #placed > 0 do
        coins.remove(placed[1])
    end
end

return coins
```
```luau
-- arena.luau
--!strict
-- The arena: a round grass floor with a fence on its rim.

local arena = {}
arena.RADIUS = 12
arena.CENTER = vec3(0.5, 65, 0.5)

world.on_generate(function(chunk)
    for x = chunk.min.x, chunk.max.x do
        for z = chunk.min.z, chunk.max.z do
            local d = math.sqrt(x * x + z * z)
            if d <= arena.RADIUS then
                chunk:set(vec3(x, 64, z), "grass_block")
            elseif d <= arena.RADIUS + 1.5 then
                chunk:set(vec3(x, 64, z), "stone_bricks")
                chunk:set(vec3(x, 65, z), "oak_fence")
            end
        end
    end
end)

-- A random block on the floor, two blocks in from the fence.
function arena.spot(): vector
    local r = arena.RADIUS - 2
    while true do
        local x, z = math.random(-r, r), math.random(-r, r)
        if x * x + z * z <= r * r then
            return vec3(x, 65, z)
        end
    end
end

return arena
```
## Try this next
- Make one coin in ten a diamond plate worth five coins: pick the block
in `coins.place`, and pass the value to `on_take`.
- Show the three best scores of all time on the sidebar under the live
scores, with `storage.keys("best.")`.
- Give the winner a golden title in chat for the next round with
`player.data`.
Next, **Parkour, a room each** gives every player a world of their own.


===== GUIDE: parkour-a-room-each | Parkour, a room each =====

## What you build
- A lobby: a small platform, and a title that says to type `/play`.
- `/play` makes a room with a random course of twelve jumps. Every fourth
jump is a gold checkpoint; the last one is an emerald.
- A timer above the hotbar, from the start to the emerald.
- Fall, and you are back at the last checkpoint.
- `/leave` goes back to the lobby; finishing does too, after the time
shows.
This guide builds on **Coin rush**: modules, `player.data`, zones and
`storage`.
## 1. The pack and the lobby
```yaml
# citadel.yml
name: parkour
entry: main.luau
motd: Parkour, a room each
spawn_point: [0.5, 65.0, 0.5]
gamemode: 2
mode: lite
world: script
```
The lobby is the main room, the one every player joins first:
```luau
-- main.luau
world.on_generate(function(chunk)
    chunk:fill(vec3(-3, 64, -3), vec3(3, 64, 3), "quartz_block") -- clipped to the chunk
end)

players.on_join(function(player)
    player.ui.title{ title = "Parkour", subtitle = "Type /play", color = "green" }
    local best = storage.get("best." .. player.uuid)
    if best then
        player:message(`Your best time is {string.format("%.1f s", best)}.`, "green")
    end
end)
```
`chunk:fill` with corners outside the chunk is clipped to it, so one line
makes a 7 by 7 platform whichever chunk asks.
## 2. A course
A course is two lists: every block to place, and the pads a player lands
on, in order.
```luau
-- course.luau
function course.make(jumps: number)
    local blocks = {} -- every block of the course: { at, block }
    local pads = {} -- where a player lands, in order: { at, kind }

    for x = -1, 1 do
        for z = -1, 1 do
            table.insert(blocks, { at = vec3(x, 64, z), block = "quartz_block" })
        end
    end

    local at = vec3(0, 64, 0)
    for i = 1, jumps do
        -- Up one block is a short jump; level or down is a longer one.
        local up = math.random(-1, 1)
        local forward = if up == 1 then 2 else 3
        at = vec3(at.x + math.random(-1, 1), math.clamp(at.y + up, 62, 70), at.z + forward)
        local kind = if i == jumps then "finish" elseif i % 4 == 0 then "checkpoint" else "jump"
        local block = if kind == "finish" then "emerald_block" elseif kind == "checkpoint" then "gold_block" else "stone_bricks"
        table.insert(blocks, { at = at, block = block })
        table.insert(pads, { at = at, kind = kind })
    end
    return { blocks = blocks, pads = pads, finish = at }
end
```
- A jump one block up is two blocks forward; a level jump or a drop is
three. A running jump makes every one of them.
- `math.clamp` keeps the course between y = 62 and y = 70.
- The pad’s kind decides its block: stone bricks, a gold checkpoint, or the
emerald finish.
The course is random, but it is made **once**, before the room exists.
That matters for the next step.
## 3. A room of its own
`rooms.create` makes a world with its own chunks, players and effects:
```luau
-- run.luau
local c = course.make(12)
local room = rooms.create{
    spawn_point = vec3(0.5, 65, 0.5),
    -- The same blocks every time: the course was made once, above.
    generate = function(chunk)
        for _, b in c.blocks do
            chunk:set(b.at, b.block) -- a block outside this chunk is ignored
        end
    end,
}
```
A room’s `generate` works like `world.on_generate`: it must make the same
blocks every time a chunk loads. It does, because it only reads the course
that was made above. `chunk:set` ignores a block outside the chunk, so the
function can hand every chunk the whole course.
## 4. The timer
```luau
-- run.luau
local started = time.now()
local respawn = vec3(0.5, 65, 0.5)
local timer = time.every(0.1, function()
    player.ui.actionbar(seconds(time.now() - started), "yellow")
end)
```
`time.now()` is seconds since the pack started; the difference is the
run’s time. Ten times a second the action bar shows it. `time.every` gives
back a connection: `timer:cancel()` stops it later.
## 5. Checkpoints and falls
```luau
-- run.luau
-- A zone checks a player's feet, one point. One block wider than the
-- pad each way, so a landing on its edge counts too.
local function above(at: vector): (vector, vector)
    return at + vec3(-1, 1, -1), at + vec3(1, 2, 1)
end

for _, pad in c.pads do
    if pad.kind == "checkpoint" then
        local from, to = above(pad.at)
        room.world.zone{ from = from, to = to, on_enter = function(p)
            if respawn ~= pad.at + vec3(0.5, 1, 0.5) then
                respawn = pad.at + vec3(0.5, 1, 0.5)
                p:message("Checkpoint!", "gold")
                room.sound.play("block.note_block.bell", { at = pad.at })
            end
        end }
    end
end

-- Everything under the course is a zone: fall into it, and go back.
room.world.zone{ from = vec3(-40, 30, -10), to = vec3(40, 58, c.finish.z + 10), on_enter = function(p)
    p:teleport(respawn)
end }
```
- Each checkpoint is a zone just above its gold block. Walking in moves
`respawn` there, once.
- A zone checks a player’s feet, which is one point. `above` makes each
zone one block wider than its pad, so a player who lands on the edge
still counts.
- One big zone fills the air under the whole course. Falling into it
teleports the player back to `respawn`: no fall damage, no death
screen.
## 6. The finish
```luau
-- run.luau
local done = false
local from, to = above(c.finish)
room.world.zone{ from = from, to = to, on_enter = function(p)
    if done then return end
    done = true
    timer:cancel()
    local t = time.now() - started
    local key = "best." .. p.uuid
    local best = storage.get(key)
    if best == nil or t < best then
        storage.set(key, t)
        p:message(`New best time: {seconds(t)}!`, "green")
    end
    p.ui.title{ title = seconds(t), subtitle = "Finished!", color = "green" }
    room.fx.particle("firework", c.finish + vec3(0.5, 2, 0.5), { count = 50, spread = 1.5, speed = 0.1 })
    task.wait(3)
    p:move_to(rooms.main)
end }
```
`done` makes the finish count once. The time is compared with the
player’s best in `storage`: a lower time is better, and `nil` means no
time yet. After three seconds of fireworks, the player goes back to the
lobby: `rooms.main` is the room everyone starts in.
## 7. Leaving, and cleaning up
```luau
-- run.luau
room.commands.add("leave", function(p)
    p:move_to(rooms.main)
end, { help = "Back to the lobby" })

room.players.on_join(function(p)
    p.ui.title{ title = "GO!", subtitle = "Reach the emerald", color = "green", stay = 1 }
end)
room.players.on_leave(function()
    timer:cancel()
    if room.players.count() == 0 then
        room:destroy()
    end
end)
player:move_to(room)
```
- `room.commands` adds a command that works only in this room: `/leave`.
- A room’s own `on_join` runs when a player moves in. Add it **before**
`move_to`, or it misses the player it was written for.
- When the last player leaves, the timer stops and `room:destroy()` frees
the world.
And the command that starts it all:
```luau
-- main.luau
commands.add("play", function(player)
    run.start(player)
end, { help = "Run a new course" })
```
## The whole pack
```luau
-- run.luau
--!strict
-- One run: a room of its own with a new course, a timer, checkpoints, a
-- floor of air that sends a faller back, and a finish.

local course = require("course")

local run = {}

local function seconds(t: number): string
    return string.format("%.1f s", t)
end

function run.start(player)
    local c = course.make(12)
    local room = rooms.create{
        spawn_point = vec3(0.5, 65, 0.5),
        -- The same blocks every time: the course was made once, above.
        generate = function(chunk)
            for _, b in c.blocks do
                chunk:set(b.at, b.block) -- a block outside this chunk is ignored
            end
        end,
    }

    local started = time.now()
    local respawn = vec3(0.5, 65, 0.5)
    local timer = time.every(0.1, function()
        player.ui.actionbar(seconds(time.now() - started), "yellow")
    end)

    -- A zone checks a player's feet, one point. One block wider than the
    -- pad each way, so a landing on its edge counts too.
    local function above(at: vector): (vector, vector)
        return at + vec3(-1, 1, -1), at + vec3(1, 2, 1)
    end

    for _, pad in c.pads do
        if pad.kind == "checkpoint" then
            local from, to = above(pad.at)
            room.world.zone{ from = from, to = to, on_enter = function(p)
                if respawn ~= pad.at + vec3(0.5, 1, 0.5) then
                    respawn = pad.at + vec3(0.5, 1, 0.5)
                    p:message("Checkpoint!", "gold")
                    room.sound.play("block.note_block.bell", { at = pad.at })
                end
            end }
        end
    end

    -- Everything under the course is a zone: fall into it, and go back.
    room.world.zone{ from = vec3(-40, 30, -10), to = vec3(40, 58, c.finish.z + 10), on_enter = function(p)
        p:teleport(respawn)
    end }

    local done = false
    local from, to = above(c.finish)
    room.world.zone{ from = from, to = to, on_enter = function(p)
        if done then return end
        done = true
        timer:cancel()
        local t = time.now() - started
        local key = "best." .. p.uuid
        local best = storage.get(key)
        if best == nil or t < best then
            storage.set(key, t)
            p:message(`New best time: {seconds(t)}!`, "green")
        end
        p.ui.title{ title = seconds(t), subtitle = "Finished!", color = "green" }
        room.fx.particle("firework", c.finish + vec3(0.5, 2, 0.5), { count = 50, spread = 1.5, speed = 0.1 })
        task.wait(3)
        p:move_to(rooms.main)
    end }

    room.commands.add("leave", function(p)
        p:move_to(rooms.main)
    end, { help = "Back to the lobby" })

    room.players.on_join(function(p)
        p.ui.title{ title = "GO!", subtitle = "Reach the emerald", color = "green", stay = 1 }
    end)
    room.players.on_leave(function()
        timer:cancel()
        if room.players.count() == 0 then
            room:destroy()
        end
    end)
    player:move_to(room)
end

return run
```
```luau
-- course.luau
--!strict
-- A course: a start pad, then a line of jumps, every fourth one a
-- checkpoint, the last one the finish. Made once per run.

local course = {}

function course.make(jumps: number)
    local blocks = {} -- every block of the course: { at, block }
    local pads = {} -- where a player lands, in order: { at, kind }

    for x = -1, 1 do
        for z = -1, 1 do
            table.insert(blocks, { at = vec3(x, 64, z), block = "quartz_block" })
        end
    end

    local at = vec3(0, 64, 0)
    for i = 1, jumps do
        -- Up one block is a short jump; level or down is a longer one.
        local up = math.random(-1, 1)
        local forward = if up == 1 then 2 else 3
        at = vec3(at.x + math.random(-1, 1), math.clamp(at.y + up, 62, 70), at.z + forward)
        local kind = if i == jumps then "finish" elseif i % 4 == 0 then "checkpoint" else "jump"
        local block = if kind == "finish" then "emerald_block" elseif kind == "checkpoint" then "gold_block" else "stone_bricks"
        table.insert(blocks, { at = at, block = block })
        table.insert(pads, { at = at, kind = kind })
    end
    return { blocks = blocks, pads = pads, finish = at }
end

return course
```
```luau
-- main.luau
--!strict
-- Parkour, a room each: the lobby, and the command that starts a run.

local run = require("run")

world.on_generate(function(chunk)
    chunk:fill(vec3(-3, 64, -3), vec3(3, 64, 3), "quartz_block") -- clipped to the chunk
end)

players.on_join(function(player)
    player.ui.title{ title = "Parkour", subtitle = "Type /play", color = "green" }
    local best = storage.get("best." .. player.uuid)
    if best then
        player:message(`Your best time is {string.format("%.1f s", best)}.`, "green")
    end
end)

commands.add("play", function(player)
    run.start(player)
end, { help = "Run a new course" })
```
## Try this next
- Show the lobby a leaderboard of best times in the sidebar, with
`storage.keys("best.")`.
- Let two friends race: `/race <name>` moves both players into one room,
and the first to the emerald wins.
- Make the course harder as it goes: longer jumps after each checkpoint.
Next, **Build a cottage** shows how to build something that looks
handmade.


===== GUIDE: your-first-pack | Your first pack =====

## Before you start
You need Minecraft Java Edition, a text editor, and a Citadel server you
can run or edit. On your own machine, the commands below assume the
`citadel` executable is on your `PATH`. If you built it from source, use
the path to `target/release/citadel` instead.
A **pack** is a folder containing configuration and Luau scripts. Citadel
runs those scripts on the server; players join with their normal Minecraft
client. You do not need to compile the scripts or install a client mod.
This guide uses **lite mode**, where your pack supplies the world and the
game’s behaviour. By the end, a player will spawn on a gold block, see a
welcome, and be able to walk away and return with `/spawn`.
## 1. Create the two files
Make a folder named `first`. Inside it, create these two files:
```text
first/
  citadel.yml
  main.luau
```
Put this in `citadel.yml`:
```yaml
# citadel.yml
name: first
entry: main.luau
motd: My first Citadel pack
spawn_point: [0.5, 65.0, 0.5]
gamemode: 2
mode: lite
world: script
```
| Setting | What it does here |
| --- | --- |
| `name` | Names this pack `first`. |
| `entry` | Tells Citadel to run `main.luau` when the pack loads. |
| `motd` | Sets the description shown in Minecraft’s server list. |
| `spawn_point` | Places a joining player’s feet at x = 0.5, y = 65, z = 0.5. |
| `gamemode: 2` | Uses adventure mode, so players can explore without breaking the floor. |
| `mode: lite` | Selects a game controlled by your scripts. |
| `world: script` | Asks your script to generate the terrain. |
This is the **pack’s** `citadel.yml`. A separate `citadel.yml` in the
directory where you start the server configures things such as its port.
Keep the pack inside `first`, and run the local commands below from the
directory containing `first`.
Start `main.luau` with `--!strict`. This enables strict checking in an
editor configured with Citadel’s `citadel.d.luau` type definitions. The
pack can run without that editor setup.
## 2. Give players ground to stand on
Add this below `--!strict` in `main.luau`:
```luau
-- main.luau
world.on_generate(function(chunk)
    chunk:fill(
        vec3(chunk.min.x, 64, chunk.min.z),
        vec3(chunk.max.x, 64, chunk.max.z),
        "stone"
    )
    chunk:set(vec3(0, 64, 0), "gold_block")
end)
```
Minecraft divides the world into **chunks**, each 16 blocks wide and 16
blocks deep. `world.on_generate` registers a function that Citadel calls
when it needs a chunk’s terrain. The `chunk` argument is the chunk being
built.
`vec3(x, y, z)` describes a position: x and z are horizontal; y is height.
`chunk:fill` fills the box between two corners, including both corners.
Using the chunk’s x and z bounds and y = 64 for both corners makes a stone
floor one block thick. Every generated chunk gets that floor.
`chunk:set` replaces one floor block with gold. It ignores coordinates
outside the current chunk, so only the chunk containing `(0, 64, 0)` gets
the marker. The spawn point is one block above it; the `.5` coordinates
place the player in the centre of the block.
Keep terrain generation repeatable: the same chunk should receive the same
blocks each time the function is called.
## 3. Run the pack and join
From the directory containing `first`, run:
```sh
citadel --lite --pack ./first
```
Leave that terminal open. In Minecraft, choose **Multiplayer → Direct
Connection**, enter `localhost:25565`, and join. If your server uses a
different port, use that port instead.
On a hosted Minefort server, put the `first` folder in the server’s `packs`
directory, select lite mode, and start the server. Join using the address
shown for that server.
**Check:** you should stand on a gold block surrounded by a flat stone
floor. Walk a few blocks and look back at the marker. There is no welcome
message or `/spawn` command yet; you will add those next.
## 4. Welcome each player
Append this after the terrain code:
```luau
-- main.luau
players.on_join(function(player)
    player.ui.title{
        title = "Welcome",
        subtitle = player.name,
        color = "aqua",
    }
    player:message("Walk around, then type /spawn to return to the gold block.", "aqua")
end)
```
`players.on_join` registers another function, this time for a player joining.
Citadel passes that player into the function as `player`. `player.name`
reads their name; `player.ui.title` shows them a title; `player:message`
sends them a chat message. These calls address that one player.
The code inside the function runs when the event happens. Register the
function once at the top level of the script; you do not need a loop that
keeps checking for new players.
Save `main.luau` while connected. Citadel reloads the script and runs its
join callbacks for players already online too.
**Check:** a “Welcome” title should appear with your name underneath it,
and chat should explain `/spawn`. That command is the next step.
## 5. Add a command that does something
Append this below the welcome code:
```luau
-- main.luau
commands.add("spawn", function(player)
    player:teleport(world.spawn_point)
    player:message("You are back at spawn.", "green")
end, { help = "Return to the lobby spawn" })
```
`commands.add` registers the name `"spawn"` without the slash. When a player
types `/spawn`, Citadel calls the function with the player who used it.
The `help` text describes the command.
`world.spawn_point` reads the spawn configured in `citadel.yml`, so you do
not need to repeat its coordinates in the script. `player:teleport` moves
the player there, and the message confirms the action.
Notice the colon in `player:teleport(...)` and `chunk:fill(...)`: these are
methods acting on a particular player or chunk. Namespace functions such
as `commands.add(...)` and `player.ui.title(...)` use a dot. Follow the
signature shown in the reference when using a new API.
**Check:** save, walk away from the gold block, and type `/spawn`. You
should return to the marker and see “You are back at spawn.” in chat.
## 6. Make a change and check it
Change `title = "Welcome"` to `title = "My lobby"`, then save. The new title
should appear without disconnecting you. Try `/spawn` again to confirm the
rest of the pack still works.
A script reload keeps the existing world. Changing the floor in
`world.on_generate` affects newly generated chunks; it does not repaint the
stone already around you. Restart after changing the pack manifest.
If a step does not work, check the server log first:
| What you see | What to check |
| --- | --- |
| The server cannot find the pack | Run from the directory containing `first`, or pass the full folder path to `--pack`. |
| You cannot connect | Keep the server running and use its configured address and port. |
| There is no floor | Check `world: script`, the `entry` filename, and any error reported while loading `main.luau`. |
| `/spawn` is unknown | Check that you saved the command block in the loaded pack and that the script reloaded successfully. |
| An edit does not take effect | Look for a filename and line number in the log. If loading the new script fails, Citadel keeps the previous working script. |
## The complete script
Your final `main.luau` should look like this. Use it to compare with your
file, or replace the file with it; do not append a second copy.
```luau
-- main.luau
--!strict
-- A small lobby: solid ground, a welcome, and a way back to spawn.

world.on_generate(function(chunk)
    chunk:fill(
        vec3(chunk.min.x, 64, chunk.min.z),
        vec3(chunk.max.x, 64, chunk.max.z),
        "stone"
    )
    chunk:set(vec3(0, 64, 0), "gold_block")
end)

players.on_join(function(player)
    player.ui.title{
        title = "Welcome",
        subtitle = player.name,
        color = "aqua",
    }
    player:message("Walk around, then type /spawn to return to the gold block.", "aqua")
end)

commands.add("spawn", function(player)
    player:teleport(world.spawn_point)
    player:message("You are back at spawn.", "green")
end, { help = "Return to the lobby spawn" })
```
You have used three entry points: terrain generation for the world,
`players.on_join` for a player’s arrival, and `commands.add` for an action
the player chooses.
## Try this next
- Change the welcome text and its colour, save, and check the result.
- Add a `/hello` command that sends a message to the player who uses it.
- Add another gold marker in the terrain function, then look for it in a
newly generated chunk.
Continue with **Coin rush** to add an objective, a score, and repeating
rounds. It builds on the pack structure and event callbacks you used here.
