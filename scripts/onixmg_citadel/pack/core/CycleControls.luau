--!nonstrict
-- core/CycleControls.luau
-- One purpose: the admin-facing controls that steer the cycle — start,
-- stop, skipVote (the /startgame cut-to-five-seconds) and setTimer. They
-- mutate GameState and wake or spawn the CycleLoop; the loop itself
-- lives in core/CycleLoop.

local state = require("core/GameState")
local Arena = require("core/Arena")
local Messages = require("core/Messages")
local Sidebar = require("ui/Sidebar")
local ActionBar = require("ui/ActionBar")
local Sound = require("util/Sound")
local Lobby = require("core/Lobby")
local CycleLoop = require("core/CycleLoop")

local CycleControls = {}

-- /startgame: cut the vote to five seconds, play the bass note and name
-- who skipped.
function CycleControls:skipVote(p)
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
function CycleControls:setTimer(n, who)
    if n and n > 0 then
        state:set_timer(n)
        Messages.debug("Admin " .. (who and who.name or "?") .. " set timer to " .. state.timer .. " seconds")
        Sidebar.refresh()
    end
end

function CycleControls:stop()
    if not state.running then return false end
    state:bump_gen()
    -- Wake the loop if it is parked in Loading: the gen bump alone cannot
    -- (coroutine.yield is not scheduler-resumed), so it sees the new gen,
    -- exits and clears running.
    state:wake()
    state.phase = "Disabled"
    state.active = nil
    state:clear_roster()
    state.timer = 0
    state:reset_votes()
    Arena:show("lobby")
    for _, p in players.list() do Lobby.send(p) end
    ui.sidebar(false)
    ActionBar.clear()
    Sound.bass()
    Messages.broadcast("System shutdown!", "gray")
    return true
end

function CycleControls:start()
    if state.running then return false end
    state.phase = "Loading"
    task.spawn(function() CycleLoop:run() end)
    return true
end

return CycleControls
