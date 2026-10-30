--!nonstrict
-- core/CycleLoop.luau
-- One purpose: the round cycle itself — Loading (parked on the join event
-- when the server is empty), the 30-second vote, then one round via
-- RoundRunner and its result via ResultSequence, repeated until the
-- generation changes (stop). Started by CycleControls.start.

local Constants = require("state/Constants")
local state = require("core/GameState")
local VoteBook = require("core/VoteBook")
local Arena = require("core/Arena")
local Messages = require("core/Messages")
local Sidebar = require("ui/Sidebar")
local ActionBar = require("ui/ActionBar")
local Sound = require("util/Sound")
local Lobby = require("core/Lobby")
local RoundRunner = require("core/RoundRunner")
local ResultSequence = require("core/ResultSequence")

local CycleLoop = {}

function CycleLoop:run()
    state:bump_gen()
    local gen = state.gen
    state.running = true

    while state.gen == gen do
        -- Loading: park on the player-join event when the server is
        -- empty, instead of polling. The only way players.count() can
        -- rise above zero is a join, so GameState:wake() (from the join
        -- handler, or from stop with a bumped gen) is the sole wake-up.
        -- A task-spawn'd thread suspended via coroutine.yield is not
        -- scheduler-resumed, so this is a true wait, not a spin.
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
        for _, p in players.list() do Lobby.send(p) end

        -- The vote: 30 s, the list read out at 30/20/10, a note every
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

        RoundRunner:run(name, gen)
        if state.gen ~= gen then break end
        ResultSequence:run(gen)
    end

    state.running = false
    Sidebar.refresh()
end

return CycleLoop
