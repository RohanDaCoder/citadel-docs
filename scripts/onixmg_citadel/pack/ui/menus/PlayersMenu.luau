--!nonstrict
-- ui/menus/PlayersMenu.luau
-- One purpose: the admin panel's players submenu — the roster's heads in
-- the classic 4-row grid slots, back at 31, each head opening the player
-- card.

local state = require("core/GameState")
local kit = require("ui/MenuKit")
local PlayerCardMenu = require("ui/menus/PlayerCardMenu")

local PlayersMenu = {}

local SLOTS = { 10, 11, 12, 13, 14, 15, 16, 19, 20, 21, 23, 24, 25, 28, 29, 30, 32, 33, 34 }

function PlayersMenu.open(p)
    local items = {}

    for i, target in state.roster do
        local slot = SLOTS[i]
        if not slot then break end
        items[slot] = kit.head(target.name)
    end

    items[31] = kit.back_item("Return to admin panel")

    kit.open_sound(p)
    p.ui.menu{
        title = { { "Players", color = "gray", bold = true } },
        items = kit.pad(items, 4),
        on_pick = function(who, n)
            if n == 31 then
                -- Required lazily: back-link to the admin panel.
                require("ui/menus/AdminMenu").open(who)
                return
            end
            for i, slot in SLOTS do
                if slot == n then
                    local target = state.roster[i]
                    if target then PlayerCardMenu.open(who, target) end
                    return
                end
            end
        end,
    }
end

return PlayersMenu
