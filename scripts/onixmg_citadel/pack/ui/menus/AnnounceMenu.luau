--!nonstrict
-- ui/menus/AnnounceMenu.luau
-- One purpose: the announcements submenu — broadcast the Discord link or
-- the vote list to everyone, back to the admin panel. The horn in the
-- middle is the menu's title piece; the two wools and the Back line act.

local Messages = require("core/Messages")
local VoteBook = require("core/VoteBook")
local kit = require("ui/MenuKit")

local AnnounceMenu = {}

function AnnounceMenu.open(p)
    kit.menu(p, {
        title = { { "Announcements", color = "gray", bold = true } },
        rows = 3,
        content = {
            { items = {
                {
                    key = "discord",
                    item = "blue_wool",
                    name = { { "Discord", color = "blue", bold = true } },
                    lore = { "Broadcast the Discord link to all players" },
                },
                { item = "goat_horn", name = { { "Announcements", color = "yellow", bold = true } }, glint = true },
                {
                    key = "vote",
                    item = "green_wool",
                    name = { { "Vote Menu", color = "green", bold = true } },
                    lore = { "Broadcast the vote menu to all players" },
                },
            }, spacing = 1 },
        },
        back = "Return to admin panel",
        on_pick = function(who, key)
            if key == "discord" then
                Messages.discord_broadcast()
                sound.play("entity.experience_orb.pickup", { volume = 0.5, pitch = 1 })
            elseif key == "vote" then
                VoteBook.announce()
            elseif key == "back" then
                -- Required lazily: back-link to the admin panel, which
                -- top-level-requires this file.
                require("ui/menus/AdminMenu").open(who)
            end
        end,
    })
end

return AnnounceMenu
