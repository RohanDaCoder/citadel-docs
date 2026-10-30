--!nonstrict
-- core/Eliminator.luau
-- One purpose: eliminate a player from the running round — announced,
-- out of the roster, back to the lobby point (unless they just left),
-- with the lava sound for everyone. `gone` skips the teleport half for a
-- player who is no longer online.

local state = require("core/GameState")
local Messages = require("core/Messages")
local Stats = require("core/Stats")
local Sound = require("util/Sound")
local Lobby = require("core/Lobby")

local Eliminator = {}

function Eliminator:eliminate(p, gone)
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
        Lobby.send(p)
    end
    Sound.lava()
    return true
end

return Eliminator
