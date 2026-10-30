--!nonstrict
-- core/Lobby.luau
-- One purpose: send a player to the lobby state — adventure mode, full
-- health, the lobby spawn point, the lobby hotbar. Used by the join and
-- respawn handlers, the eliminator, the cycle controls, the result
-- sequence, the void safety net and /spawn.

local Arena = require("core/Arena")
local Hotbar = require("ui/Hotbar")

local Lobby = {}

function Lobby.send(p)
    p.gamemode = 2
    p.health = 20
    Arena:send(p, "lobby")
    Hotbar.lobby(p)
end

return Lobby
