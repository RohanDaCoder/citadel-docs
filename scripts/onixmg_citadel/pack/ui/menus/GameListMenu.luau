--!nonstrict
-- ui/menus/GameListMenu.luau
-- One purpose: the profile's game list — a card per registered game
-- (votable or not), walked from slot 10 and skipping 13 (the head
-- column), with Back to the profile. Re-derives which game a picked
-- slot holds with the same walk.

local Stats = require("core/Stats")
local registry = require("core/GameRegistry")
local kit = require("ui/MenuKit")
local GameStatMenu = require("ui/menus/GameStatMenu")

local GameListMenu = {}

function GameListMenu.open(viewer, target)
    local uuid = target.uuid
    local items = {}

    local slot = 10
    for _, name in registry:all() do
        local g = registry:get(name)
        if slot == 13 then slot = slot + 1 end
        local played = Stats.stat(uuid, "played." .. g.key)
        local wins = Stats.stat(uuid, "wins." .. g.key)
        local rate = played > 0 and math.floor(wins / played * 100 + 0.5) or 0
        items[slot] = {
            item = g.icon or "paper",
            name = { { g.name, color = "aqua", bold = true } },
            lore = {
                { { "Played: ", color = "gray" }, { tostring(played), color = "white" } },
                { { "Wins: ", color = "gray" }, { tostring(wins), color = "white" } },
                { { "Win Rate: ", color = "gray" }, { rate .. "%", color = "white" } },
            },
            glint = true,
        }
        slot = slot + 1
    end

    items[22] = kit.back_item("Return to profile")

    kit.open_sound(viewer)
    viewer.ui.menu{
        title = {
            { "Game Stats", color = "gray", bold = true },
            { " - ", color = "gray" },
            { target.name, color = "white" },
        },
        items = kit.pad(items, 3),
        on_pick = function(who, n)
            if n == 22 then
                -- Required lazily: this menu links back to the profile,
                -- and a top-level require would be circular.
                require("ui/menus/ProfileMenu").open(who, target)
                return
            end
            -- Re-derive which game landed on the picked slot.
            local slot = 10
            for _, name in registry:all() do
                if slot == 13 then slot = slot + 1 end
                if slot == n then
                    GameStatMenu.open(who, target, registry:get(name))
                    return
                end
                slot = slot + 1
            end
        end,
    }
end

return GameListMenu
