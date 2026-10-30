--!nonstrict
-- core/CycleDriver.luau
-- The round-cycle orchestrator. Owns the Loading -> Lobby -> Ingame ->
-- Result loop and the controls that steer it (start, stop, skipVote,
-- setTimer, eliminate, onJoin). All shared state lives on GameState;
-- the votable games on GameRegistry; the maps on Arena. One instance
-- exists for the whole pack; subsystems require this module and call its
-- methods on the returned singleton.
--
-- When the server is empty the Loading phase parks on the player-join
-- event instead of polling: onJoin is the sole wake-up, and stop bumps
-- gen and resumes the parked coroutine so a shutdown while empty does
-- not strand the loop.

local Constants = require("state/Constants")
local state = require("core/GameState")
local registry = require("core/GameRegistry")
local VoteBook = require("core/VoteBook")
local Arena = require("core/Arena")
local Messages = require("core/Messages")
local Stats = require("core/Stats")
local Sidebar = require("ui/Sidebar")
local ActionBar = require("ui/ActionBar")
local Titles = require("ui/Titles")
local Sound = require("util/Sound")
local Hotbar = require("ui/Hotbar")

local CycleDriver = {}
CycleDriver.__index = CycleDriver

-- The old spawn(): the lobby point, wherever the current map puts it.
function CycleDriver:lobby(p)
    p.gamemode = 2
    p.health = 20
    Arena:send(p, "lobby")
    Hotbar.lobby(p)
end

function CycleDriver:onJoin(p)
    self:lobby(p)
    Sidebar.refresh()
    -- If the cycle loop is parked in Loading waiting for the first
    -- player, this join is its sole wake-up. Resume on the next
    -- scheduler tick so onJoin itself stays non-blocking.
    local waiter = state:take_waiter()
    if waiter and coroutine.status(waiter) == "suspended" then
        task.spawn(function() coroutine.resume(waiter) end)
    end
end

-- Eliminate: out of the round, back to the lobby point, with the lava
-- sound the old server played for everyone. `gone` skips the teleport
-- half for a player who just left.
function CycleDriver:eliminate(p, gone)
    if state.phase ~= "Ingame" then return false end
    if not state:leave_roster(p) then return false end

    Messages.broadcast_runs({
        { p.name, color = "yellow" },
        { " was eliminated from the game!", color = "red" },
    })
    if not gone then
        if state.active == "TNT Run" then
            p:message({
                { "Blocks Broken: ", color = "gray" },
                { tostring(Stats.stat(p.uuid, "tntrun")), color = "yellow" },
            })
        end
        self:lobby(p)
    end
    Sound.lava()
    return true
end

-- One round: roster everyone, paste the arena, run the game's lifecycle
-- hooks, end on time or when one player is left standing.
function CycleDriver:play(name, gen)
    local game = registry:get(name)
    if not game then return end

    state.phase = "Ingame"
    state.active = name
    state:clear_roster()

    Sound.levelup()
    Titles.loading()

    -- Everyone playing is rostered, counted and sent to the lobby point
    -- first, adventure mode included.
    for _, p in players.list() do
        state:add_to_roster(p)
        p.gamemode = 2
        p.health = 20
        Arena:send(p, "lobby")
        Stats.bump(p.uuid, "played")
        Stats.bump(p.uuid, "played." .. game.key)
    end

    Arena:show(game.arena)
    task.wait(3)

    -- "&e&lSpleef &8- &fDig your way to victory!" — a plain broadcast, no
    -- prefix, each game in its own colour.
    message({
        { name, color = game.title_color or "yellow", bold = true },
        { " - ", color = "dark_gray" },
        { game.blurb or "", color = "white" },
    })
    local spawn = Arena:spawn(game.arena)
    local yaw = Arena:yaw(game.arena)
    for _, p in state.roster do
        p:teleport(spawn, { yaw = yaw, pitch = 0 })
    end

    game:onStart()

    local remaining = game.duration or Constants.ROUND_SECONDS
    local acc = 0
    state.timer = math.ceil(remaining)
    Sidebar.refresh()

    -- The round ends on time, or as soon as one player is left standing.
    -- The void check is the per-game void_y, only the games that had one.
    while state.gen == gen and remaining > 0 and #state.roster > 1 do
        if state.timer_override then
            remaining = state.timer_override
            state.timer_override = nil
        end
        local dt = task.wait(0.05)
        remaining = remaining - dt

        game:onStep(dt)

        if game.void_y then
            for i = #state.roster, 1, -1 do
                local p = state.roster[i]
                local at = p.at
                if at and at.y < game.void_y then self:eliminate(p) end
            end
        end

        acc = acc + dt
        if acc >= 0.25 then
            acc = 0
            state.timer = math.max(math.ceil(remaining), 0)
            Sidebar.refresh()
            ActionBar.active(name, state.timer)
        end
    end

    game:onStop()
end

-- The result sequence: winner card, the hold, the return to lobby, and
-- the closing pair that ends every cycle.
function CycleDriver:finish(gen)
    state.phase = "Result"
    state.timer = 10

    -- Nobody left is "&8[&7Nobody&8]"; anyone left is the first player of
    -- the list in order.
    local winner = nil
    if #state.roster > 0 then
        winner = state.roster[1]
    end

    local name_runs
    if winner then
        name_runs = { { winner.name, color = "green" } }
    else
        name_runs = {
            { "[", color = "dark_gray" },
            { "Nobody", color = "gray" },
            { "]", color = "dark_gray" },
        }
    end

    if winner then
        local game = registry:get(state.active)
        Stats.bump(winner.uuid, "wins")
        if game then Stats.bump(winner.uuid, "wins." .. game.key) end
    end

    Messages.broadcast_runs(Messages.cat(name_runs, { { " is The Winner", color = "yellow" } }))
    Titles.winner(name_runs)
    Sound.toast()

    task.wait(Constants.RESULT_HOLD)

    Messages.broadcast("Returning to lobby...", "gray")
    Arena:show("lobby")
    task.wait(Constants.RESULT_RETURN)

    state:clear_roster()
    state.active = nil
    for _, p in players.list() do
        self:lobby(p)
    end

    if state.gen ~= gen then return end

    Messages.broadcast_runs({ { "The game has ended!", color = "red", bold = true } })
    message("")
    task.wait(Constants.RESULT_GAP)
end

-- The cycle: wait for players (parked on the join event when empty), run
-- the vote, play a round, finish, repeat — until gen changes (stop).
function CycleDriver:run()
    state:bump_gen()
    local gen = state.gen
    state.running = true

    while state.gen == gen do
        state:reset_for_loading()
        Sidebar.refresh()
        if players.count() == 0 and state.gen == gen then
            citadel.log("No players to start cycle - waiting for a player to join.")
            state.cycle_waiter = coroutine.running()
            coroutine.yield()
            state.cycle_waiter = nil
        end
        if state.gen ~= gen then break end
        Messages.debug("Starting new cycle...")

        state.phase = "Lobby"
        state.skip = false
        state:reset_votes()
        Arena:show("lobby")
        for _, p in players.list() do self:lobby(p) end

        -- The vote: 30s, the list read out at 30/20/10, a note every
        -- one of the last five seconds.
        local remaining = Constants.VOTE_SECONDS
        local shown = -1
        local last_tick = -1
        while remaining > 0 and state.gen == gen do
            if state.timer_override then
                remaining = state.timer_override
                state.timer_override = nil
                shown = -1
            end
            if state.skip then
                state.skip = false
                remaining = math.min(remaining, 5)
            end
            state.timer = math.ceil(remaining)
            if state.timer ~= shown then
                shown = state.timer
                if state.timer == Constants.VOTE_SECONDS or state.timer == 20 or state.timer == 10 then
                    VoteBook.announce()
                end
                Sidebar.refresh()
            end
            if state.timer ~= last_tick then
                last_tick = state.timer
                if state.timer <= 5 then
                    Sound.bit(1, 1)
                end
            end
            ActionBar.vote_phase(state.timer)
            remaining = remaining - task.wait(0.5)
        end

        if state.gen ~= gen then break end

        local name, had_votes = VoteBook.winning()
        if had_votes then
            Messages.broadcast_runs({
                { "Selected Game: ", color = "yellow" },
                { name, color = "green", bold = true },
            })
        end
        task.wait(2)
        if state.gen ~= gen then break end

        self:play(name, gen)
        if state.gen ~= gen then break end
        self:finish(gen)
    end

    state.running = false
    Sidebar.refresh()
end

-- /startgame: the old command cut the vote to five seconds, played the
-- bass note and named who skipped.
function CycleDriver:skipVote(p)
    if state.phase ~= "Lobby" then return false end
    if state.timer <= 5 then return false end
    state.skip = true
    Sound.bass()
    Messages.broadcast_runs({
        { (p and p.name or "Someone"), color = "yellow" },
        { " skipped waiting time.", color = "gray" },
    })
    return true
end

-- /settimer <seconds>: the old command wrote the variable and only the
-- debug line ever said so.
function CycleDriver:setTimer(n, who)
    if n and n > 0 then
        state:set_timer(n)
        Messages.debug("Admin " .. (who and who.name or "?") .. " set timer to " .. state.timer .. " seconds")
        Sidebar.refresh()
    end
end

function CycleDriver:stop()
    if not state.running then return false end
    state:bump_gen()
    -- If the run loop is parked in Loading on the join event, bumping
    -- gen alone cannot wake it (coroutine.yield is not scheduler-resumed);
    -- resume it so the loop sees the new gen, exits and clears running.
    local waiter = state:take_waiter()
    if waiter then
        task.spawn(function()
            if coroutine.status(waiter) == "suspended" then coroutine.resume(waiter) end
        end)
    end
    state.phase = "Disabled"
    state.active = nil
    state:clear_roster()
    state.timer = 0
    state:reset_votes()
    Arena:show("lobby")
    for _, p in players.list() do self:lobby(p) end
    ui.sidebar(false)
    ActionBar.clear()
    Sound.bass()
    Messages.broadcast("System shutdown!", "gray")
    return true
end

function CycleDriver:start()
    if state.running then return false end
    state.phase = "Loading"
    task.spawn(function() self:run() end)
    return true
end

local driver = setmetatable({}, CycleDriver)
return driver
