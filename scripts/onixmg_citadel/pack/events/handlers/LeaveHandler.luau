--!nonstrict
-- events/handlers/LeaveHandler.luau
-- One purpose: handle the player-leave event — mid-round, the active game
-- hears it first (Hot Potato passes the potato on), then the announced
-- elimination without teleport; always the sidebar and tab refresh.

local GameState = require("core/GameState")
local GameRegistry = require("core/GameRegistry")
local Eliminator = require("core/Eliminator")
local Sidebar = require("ui/Sidebar")
local Tab = require("ui/Tab")

local LeaveHandler = {}

function LeaveHandler.handle(p)
    if GameState.phase == "Ingame" then
        local g = GameRegistry:get(GameState.active)
        if g then g:onLeave(p) end
        Eliminator:eliminate(p, true)
    end
    Sidebar.refresh()
    Tab.set(1)
end

return LeaveHandler
