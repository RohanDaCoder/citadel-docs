--!nonstrict
-- events/handlers/RespawnHandler.luau
-- One purpose: handle the respawn event — "on respawn: wait 1 tick;
-- spawn(player)": the lobby point, always, mid-game or not.
-- (Respawning into an arena's exact point would re-drop a player through
-- its light pillar every death; for Hot Potato the 30-block fall is
-- lethal and would loop.)

local Lobby = require("core/Lobby")

local RespawnHandler = {}

function RespawnHandler.handle(p)
    Lobby.send(p)
end

return RespawnHandler
