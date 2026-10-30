--!nonstrict
-- events/handlers/DamageHandler.luau
-- One purpose: handle the damage event — mid-round the active game
-- answers the damage question (Hot Potato refuses the holder's hits);
-- every other case takes its hits as the old server did.

local GameState = require("core/GameState")
local GameRegistry = require("core/GameRegistry")

local DamageHandler = {}

function DamageHandler.handle(p, hit)
    if GameState.phase == "Ingame" then
        local g = GameRegistry:get(GameState.active)
        if g then
            return g:onDamage(p, hit)
        end
    end
end

return DamageHandler
