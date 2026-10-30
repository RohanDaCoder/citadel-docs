--!nonstrict
-- ui/Sidebar.luau
-- The scoreboard sidebar: state, game, timer, alive count, and — during
-- the lobby — the live vote tally. An addition the live server lacked;
-- it keeps the vote readable without clickable chat. refresh() rebuilds
-- it from the current GameState and registry.

local state = require("core/GameState")
local registry = require("core/GameRegistry")
local Constants = require("state/Constants")

local Sidebar = {}

local function phase_label()
    if state.phase == "Lobby" then return "Voting" end
    if state.phase == "Ingame" then return "Playing" end
    if state.phase == "Result" then return "Results" end
    if state.phase == "Loading" then return "Loading" end
    return state.phase
end

function Sidebar.refresh()
    local lines = {
        { { "State   ", color = "gray" }, { phase_label(), color = "white" } },
        { { "Game    ", color = "gray" }, { state.active or "-", color = "white" } },
        { { "Timer   ", color = "gray" }, { tostring(math.max(state.timer, 0)) .. "s", color = "yellow" } },
        { { "Alive   ", color = "gray" }, { tostring(#state.roster), color = "white" } },
        "",
    }
    if state.phase == "Lobby" then
        for _, name in registry:votable() do
            table.insert(lines, {
                { name, color = "white" },
                { "  " .. state:vote_count(name), color = "green" },
            })
        end
        table.insert(lines, "")
        table.insert(lines, { { "/vote <game>", color = "yellow" } })
    end
    ui.sidebar{ title = { "ONIX MINIGAMES", color = Constants.ACCENT, bold = true }, lines = lines }
end

return Sidebar
