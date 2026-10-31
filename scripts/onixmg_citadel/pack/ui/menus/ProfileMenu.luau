--!nonstrict
-- ui/menus/ProfileMenu.luau
-- One purpose: the profile's main page — overall stats, the head, the
-- link to the per-game list, close. The stats card and the head are
-- display; the chest card and the Close line are the two keys.

local Stats = require("core/Stats")
local kit = require("ui/MenuKit")
local GameListMenu = require("ui/menus/GameListMenu")

local ProfileMenu = {}

function ProfileMenu.open(viewer, target)
    local uuid = target.uuid
    local played = Stats.stat(uuid, "played")
    local wins = Stats.stat(uuid, "wins")
    local rate = played > 0 and math.floor(wins / played * 100 + 0.5) or 0

    kit.menu(viewer, {
        title = {
            { "Profile", color = "gray", bold = true },
            { " - ", color = "gray" },
            { target.name, color = "white" },
        },
        rows = 3,
        content = {
            { items = {
                {
                    item = "diamond",
                    name = { { "Overall Stats", color = "aqua", bold = true } },
                    lore = {
                        { { "Games Played: ", color = "gray" }, { tostring(played), color = "white" } },
                        { { "Games Won: ", color = "gray" }, { tostring(wins), color = "white" } },
                        { { "Win Rate: ", color = "gray" }, { rate .. "%", color = "white" } },
                    },
                    glint = true,
                },
                {
                    item = "player_head",
                    skin = target.name,
                    name = { { target.name, color = "aqua", bold = true } },
                    lore = { "Profile" },
                },
                {
                    key = "games",
                    item = "chest",
                    name = { { "Game Statistics", color = "aqua", bold = true } },
                    lore = { "Click to browse per-game", "statistics" },
                },
            }, spacing = 1 },
        },
        close = "Click to close",
        on_pick = function(who, key)
            if key == "games" then
                GameListMenu.open(who, target)
            end
        end,
    })
end

return ProfileMenu
