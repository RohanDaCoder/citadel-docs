--!nonstrict
-- tasks/VoidSafetyTask.luau
-- One purpose: the void safety net — the arena floats well above the
-- void; nobody should ever be below y 50. A rostered player below it is
-- eliminated; anyone else is sent back to the lobby.

local GameState = require("core/GameState")
local Eliminator = require("core/Eliminator")
local Lobby = require("core/Lobby")

local VoidSafetyTask = {}

function VoidSafetyTask.start()
    task.spawn(function()
        while true do
            task.wait(1)
            for _, p in players.list() do
                local at = p.at
                if at and at.y < 50 then
                    if GameState.phase == "Ingame" and GameState:in_roster(p) then
                        Eliminator:eliminate(p)
                    else
                        Lobby.send(p)
                    end
                end
            end
        end
    end)
end

return VoidSafetyTask
