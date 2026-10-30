--!nonstrict
-- events/handlers/ClickHandler.luau
-- One purpose: handle the click event — mid-round, clicks belong to the
-- active game (rostered players only); otherwise the lobby hotbar's
-- three items: the vote compass, the profile book, the Discord paper.

local GameState = require("core/GameState")
local GameRegistry = require("core/GameRegistry")
local Messages = require("core/Messages")
local VoteMenu = require("ui/menus/VoteMenu")
local ProfileMenu = require("ui/menus/ProfileMenu")

local ClickHandler = {}

function ClickHandler.handle(p, hit)
    if GameState.phase == "Ingame" then
        local g = GameRegistry:get(GameState.active)
        if g and GameState:in_roster(p) then
            g:onClick(p, hit)
        end
        return
    end

    if hit.slot == 1 then
        VoteMenu.open(p)
    elseif hit.slot == 2 then
        ProfileMenu.open(p, p)
    elseif hit.slot == 5 then
        Messages.discord_broadcast(p)
        p:sound("entity.experience_orb.pickup", { volume = 0.5, pitch = 1 })
    end
end

return ClickHandler
