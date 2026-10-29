---
title: 'Coin rush'
description: 'Build a sixty-second arcade game — a round arena, gold plates taken by walking on them, a boss-bar countdown, live sidebar scores, and best scores kept in storage.'
---

:::note[In short]
this tutorial builds a whole game in one pack: a round arena,
five gold pressure plates that vanish when a player walks onto them, a
boss bar counting down the round, a sidebar of live scores, and a winner
with fireworks at the end. It exercises zones, `player.data`, `storage`,
tasks and the UI bars together.
:::

## What you build
- A round grass arena with a fence on its rim.
- Five gold pressure plates, the coins, at random places on the floor.
  Walk onto one to take it; a new one appears somewhere else.
- A boss bar that counts down the round, and a sidebar with every
  player's score.
- At the end: the winner's name on screen, fireworks, and a message to
  each player who beat their best.

## Before you start

Read [Quick start](/getting-started/quick-start/) first: this guide uses what it
explains.

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
requires it shares one arena (see [Runtime](/concepts/runtime/)).

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

## Try it

Run the pack and walk out from the middle: grass inside the radius, then
a stone ring with a fence on it — and the ring closes on its own, because
fences join their neighbours.

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
- [`world.zone`](/ref/World/zone/) is a box of blocks. Here it is one
  block, and `on_enter` runs when a player's feet enter it.
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
as long as the player is connected (see
[Player lifecycle](/players/player-lifecycle/)). The sidebar shows everyone's:

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

[Storage](/systems/storage/) keeps values across restarts. The key uses
`player.uuid`, not the name: a player can change their name, never their
id.

## Try it

Join with the pack running: your score starts at 0, chat tells you your
best, and the sidebar lists every player, most coins first. Rounds — which
put the coins on the floor — come next.

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
are taken, sounds play and other players join while it waits. At the end
the round finds the winner and saves each best score:

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

## Try it

Let a round run out: the boss bar drains a second at a time, the coins
clear, each player who beat their best is told so, and the winner's name
goes on screen with fireworks.

## 6. Rounds forever

One round is not a game — run them forever:

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

## Try it

Be the last one online, then leave: the loop waits, one second at a
time, until someone joins again — and a round starts straight away.

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

## Where to go next

Try:

- Make one coin in ten a diamond plate worth five coins: pick the block
  in `coins.place`, and pass the value to `on_take`.
- Show the three best scores of all time on the sidebar under the live
  scores, with `storage.keys("best.")`.
- Give the winner a golden title in chat for the next round with
  `player.data`.

Next, [Parkour, a room each](/guides/guide-parkour-a-room-each/) gives every
player a world of their own.

Then go deeper:

- [UI basics](/ui/ui-basics/) — sidebar, boss bar, titles, messages.
- [Storage](/systems/storage/) — `get`, `set`, `keys`, flushing.
- [Runtime](/concepts/runtime/) — modules, `task.spawn`, `task.wait`.
- [Player lifecycle](/players/player-lifecycle/) — `player.data` and its
  lifetime.
- [FX](/ui/fx/) and [Sound](/ui/sound/) — particles and playback.

## See also

- [Build a cottage](/guides/guide-build-a-cottage/) — building well, in code.
- [A dungeon dimension](/guides/guide-a-dungeon-dimension/) — a second world
  under the yard.
- [Cookbook: leaderboards](/cookbook/cookbook-leaderboards/) — the sidebar and
  storage pattern, alone.
