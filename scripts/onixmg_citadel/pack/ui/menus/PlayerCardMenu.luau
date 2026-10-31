--!nonstrict
-- ui/menus/PlayerCardMenu.luau
-- One purpose: the admin panel's player card — view the profile, the
-- head, eliminate, back to the player list. The head is display; the
-- book, the barrier and the Back line are the three keys.

local Messages = require("core/Messages")
local Eliminator = require("core/Eliminator")
local kit = require("ui/MenuKit")
local ProfileMenu = require("ui/menus/ProfileMenu")

local PlayerCardMenu = {}

function PlayerCardMenu.open(p, target)
    kit.menu(p, {
        title = { { target.name, color = "gray", bold = true } },
        rows = 3,
        content = {
            { items = {
                {
                    key = "profile",
                    item = "book",
                    name = { { "View Profile", color = "aqua", bold = true } },
                    lore = { "View " .. target.name .. "'s profile" },
                },
                kit.head(target.name),
                {
                    key = "eliminate",
                    item = "barrier",
                    name = { { "Eliminate", color = "red", bold = true } },
                    lore = { "Remove " .. target.name .. " from the game" },
                },
            }, spacing = 1 },
        },
        back = "Return to player list",
        on_pick = function(who, key)
            if key == "profile" then
                ProfileMenu.open(who, target)
            elseif key == "eliminate" then
                if Eliminator:eliminate(target) then
                    Messages.tell(who, target.name .. " eliminated.", "yellow")
                else
                    Messages.deny(who, "That player is not in a round.")
                end
                -- Required lazily: back to the player list, which
                -- top-level-requires this file.
                require("ui/menus/PlayersMenu").open(who)
            elseif key == "back" then
                require("ui/menus/PlayersMenu").open(who)
            end
        end,
    })
end

return PlayerCardMenu
