--!nonstrict
-- ui/menus/AnnounceMenu.luau
-- One purpose: the announcements submenu — broadcast the Discord link or
-- the vote list to everyone, back to the admin panel.

local Messages = require("core/Messages")
local VoteBook = require("core/VoteBook")
local kit = require("ui/MenuKit")

local AnnounceMenu = {}

function AnnounceMenu.open(p)
    local items = {}
    items[11] = { item = "blue_wool", name = { { "Discord", color = "blue", bold = true } }, lore = { "Broadcast the Discord link to all players" } }
    items[13] = { item = "goat_horn", name = { { "Announcements", color = "yellow", bold = true } }, glint = true }
    items[15] = { item = "green_wool", name = { { "Vote Menu", color = "green", bold = true } }, lore = { "Broadcast the vote menu to all players" } }
    items[22] = kit.back_item("Return to admin panel")

    kit.open_sound(p)
    p.ui.menu{
        title = { { "Announcements", color = "gray", bold = true } },
        items = kit.pad(items, 3),
        on_pick = function(who, n)
            if n == 11 then
                Messages.discord_broadcast()
                sound.play("entity.experience_orb.pickup", { volume = 0.5, pitch = 1 })
            elseif n == 15 then
                VoteBook.announce()
            elseif n == 22 then
                -- Required lazily: back-link to the admin panel, which
                -- top-level-requires this file.
                require("ui/menus/AdminMenu").open(who)
            end
        end,
    }
end

return AnnounceMenu
