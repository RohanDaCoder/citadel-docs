--!nonstrict
-- ui/menus/GameListMenu.luau
-- One purpose: the profile's game list — a card per registered game
-- (votable or not) with Back to the profile. The kit centers the cards;
-- a picked card comes back as the game's name.

local Stats = require("core/Stats")
local registry = require("core/GameRegistry")
local kit = require("ui/MenuKit")
local GameStatMenu = require("ui/menus/GameStatMenu")

local GameListMenu = {}

function GameListMenu.open(viewer, target)
    local uuid = target.uuid
    local cards = {}

    for _, name in registry:all() do
        local g = registry:get(name)
        local played = Stats.stat(uuid, "played." .. g.key)
        local wins = Stats.stat(uuid, "wins." .. g.key)
        local rate = played > 0 and math.floor(wins / played * 100 + 0.5) or 0
        table.insert(cards, {
            key = name,
            item = g.icon or "paper",
            name = { { g.name, color = "aqua", bold = true } },
            lore = {
                { { "Played: ", color = "gray" }, { tostring(played), color = "white" } },
                { { "Wins: ", color = "gray" }, { tostring(wins), color = "white" } },
                { { "Win Rate: ", color = "gray" }, { rate .. "%", color = "white" } },
            },
            glint = true,
        })
    end

    kit.menu(viewer, {
        title = {
            { "Game Stats", color = "gray", bold = true },
            { " - ", color = "gray" },
            { target.name, color = "white" },
        },
        rows = 3,
        content = { { items = cards, spacing = 1 } },
        back = "Return to profile",
        on_pick = function(who, key)
            if key == "back" then
                -- Required lazily: this menu links back to the profile,
                -- and a top-level require would be circular.
                require("ui/menus/ProfileMenu").open(who, target)
            else
                GameStatMenu.open(who, target, registry:get(key))
            end
        end,
    })
end

return GameListMenu
