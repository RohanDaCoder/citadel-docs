--!nonstrict
-- events/handlers/JoinHandler.luau
-- One purpose: handle the player-join event — the join sequence, in
-- order: to the lobby point, the four gold welcome lines, the tab list,
-- the one-shot spawn probe, the sidebar, and the wake-up for a cycle
-- parked in Loading waiting for the first player.

local GameState = require("core/GameState")
local Lobby = require("core/Lobby")
local Motd = require("ui/Motd")
local Tab = require("ui/Tab")
local Sidebar = require("ui/Sidebar")
local SpawnProbe = require("boot/SpawnProbe")

local JoinHandler = {}

function JoinHandler.handle(p)
    Lobby.send(p)          -- the Skript's spawn(); no welcome of its own
    Motd.welcome(p)        -- Essentials sent these next
    Tab.set(1)
    SpawnProbe.check()
    Sidebar.refresh()
    GameState:wake()       -- the parked cycle's sole wake-up (next tick)
end

return JoinHandler
