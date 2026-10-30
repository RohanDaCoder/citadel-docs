--!nonstrict
-- ui/menus/ProfileMenu.luau
-- One purpose: the profile's main page — overall stats, the head, the
-- link to the per-game list, close. Slot 15 opens the game list, as the
-- original layout had it (10 stats, 13 head, 15 game statistics, 16
-- close).

local Stats = require("core/Stats")
local kit = require("ui/MenuKit")
local GameListMenu = require("ui/menus/GameListMenu")

local ProfileMenu = {}

function ProfileMenu.open(viewer, target)
    local uuid = target.uuid
    local played = Stats.stat(uuid, "played")
    local wins = Stats.stat(uuid, "wins")
    local rate = played > 0 and math.floor(wins / played * 100 + 0.5) or 0

    local items = {}
    items[10] = {
        item = "diamond",
        name = { { "Overall Stats", color = "aqua", bold = true } },
        lore = {
            { { "Games Played: ", color = "gray" }, { tostring(played), color = "white" } },
            { { "Games Won: ", color = "gray" }, { tostring(wins), color = "white" } },
            { { "Win Rate: ", color = "gray" }, { rate .. "%", color = "white" } },
        },
        glint = true,
    }
    items[13] = {
        item = "player_head",
        skin = target.name,
        name = { { target.name, color = "aqua", bold = true } },
        lore = { "Profile" },
    }
    items[15] = {
        item = "chest",
        name = { { "Game Statistics", color = "aqua", bold = true } },
        lore = { "Click to browse per-game", "statistics" },
    }
    items[16] = kit.close_item("Click to close")

    kit.open_sound(viewer)
    viewer.ui.menu{
        title = {
            { "Profile", color = "gray", bold = true },
            { " - ", color = "gray" },
            { target.name, color = "white" },
        },
        items = kit.pad(items, 3),
        on_pick = function(who, n)
            if n == 15 then
                GameListMenu.open(who, target)
            end
        end,
    }
end

return ProfileMenu
