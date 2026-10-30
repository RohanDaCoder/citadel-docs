--!nonstrict
-- core/ResultSequence.luau
-- One purpose: the end-of-round sequence — the winner card (first roster
-- player left standing, or [Nobody]), the hold, the return to the lobby
-- map, everyone back to the lobby point, and the closing "The game has
-- ended!" pair with its blank line and gap.

local Constants = require("state/Constants")
local state = require("core/GameState")
local registry = require("core/GameRegistry")
local Messages = require("core/Messages")
local Stats = require("core/Stats")
local Arena = require("core/Arena")
local Titles = require("ui/Titles")
local Sound = require("util/Sound")
local Lobby = require("core/Lobby")

local ResultSequence = {}

function ResultSequence:run(gen)
    state.phase = "Result"
    state.timer = 10

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
        Lobby.send(p)
    end

    if state.gen ~= gen then return end

    Messages.broadcast_runs({ { "The game has ended!", color = "red", bold = true } })
    message("")
    task.wait(Constants.RESULT_GAP)
end

return ResultSequence
