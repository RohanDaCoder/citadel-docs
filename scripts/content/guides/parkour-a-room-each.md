---
title: "Parkour, a room each"
url: /docs/citadel/guides/parkour-a-room-each
---

# Parkour, a room each

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
