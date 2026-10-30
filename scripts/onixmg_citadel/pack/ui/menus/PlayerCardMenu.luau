--!nonstrict
-- ui/menus/PlayerCardMenu.luau
-- One purpose: the admin panel's player card — view the profile, the
-- head, eliminate, back to the player list.

local Messages = require("core/Messages")
local Eliminator = require("core/Eliminator")
local kit = require("ui/MenuKit")
local ProfileMenu = require("ui/menus/ProfileMenu")

local PlayerCardMenu = {}

function PlayerCardMenu.open(p, target)
    local items = {}
    items[11] = { item = "book", name = { { "View Profile", color = "aqua", bold = true } }, lore = { "View " .. target.name .. "'s profile" } }
    items[13] = kit.head(target.name)
    items[15] = { item = "barrier", name = { { "Eliminate", color = "red", bold = true } }, lore = { "Remove " .. target.name .. " from the game" } }
    items[22] = kit.back_item("Return to player list")

    kit.open_sound(p)
    p.ui.menu{
        title = { { target.name, color = "gray", bold = true } },
        items = kit.pad(items, 3),
        on_pick = function(who, n)
            if n == 11 then
                ProfileMenu.open(who, target)
            elseif n == 15 then
                if Eliminator:eliminate(target) then
                    Messages.tell(who, target.name .. " eliminated.", "yellow")
                else
                    Messages.deny(who, "That player is not in a round.")
                end
                -- Required lazily: back-link to the player list, which
                -- top-level-requires this file.
                require("ui/menus/PlayersMenu").open(who)
            elseif n == 22 then
                require("ui/menus/PlayersMenu").open(who)
            end
        end,
    }
end

return PlayerCardMenu
