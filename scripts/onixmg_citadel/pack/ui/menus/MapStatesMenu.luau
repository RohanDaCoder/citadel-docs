--!nonstrict
-- ui/menus/MapStatesMenu.luau
-- One purpose: /changemapstate's 5-row map picker — the live server's own
-- items in its own slots (the glinted beacon/shovel/TNT/head/potato with
-- "Click to change map state to <name>" lore), three barriers where the
-- next games will go, no Close (Escape closes; the old chest stayed
-- open, so it re-opens after every pick).

local state = require("core/GameState")
local Arena = require("core/Arena")
local Messages = require("core/Messages")
local Sidebar = require("ui/Sidebar")
local kit = require("ui/MenuKit")

local MapStatesMenu = {}

local STATE_ITEMS = {
    { 10, "lobby", "Lobby", "aqua", "beacon" },
    { 12, "spleef", "Spleef", "yellow", "golden_shovel" },
    { 14, "tntrun", "TNT Run", "red", "tnt" },
    { 16, "sumo", "Sumo", "dark_red", "player_head" },
    { 28, "hotpotato", "Hot Potato", "gold", "baked_potato" },
}

function MapStatesMenu.open(p)
    local items = {}

    for _, row in STATE_ITEMS do
        local slot, key, label, colr, item = row[1], row[2], row[3], row[4], row[5]
        items[slot] = {
            item = item,
            name = { { label, color = colr, bold = true } },
            glint = true,
            lore = {
                { { "Click to change map state to ", color = "gray" }, { label, color = "yellow" } },
            },
        }
    end

    local soon = {
        item = "barrier",
        name = { { "To be added..", color = "red", bold = true } },
        lore = { { "New minigames will be added here", color = "yellow" } },
    }
    items[30] = soon
    items[32] = soon
    items[34] = soon

    kit.open_sound(p)
    p.ui.menu{
        title = { { "Select Map State", color = "yellow", bold = true } },
        items = kit.pad(items, 5),
        on_pick = function(who, n)
            for _, row in STATE_ITEMS do
                if row[1] == n then
                    if state.phase == "Ingame" then
                        Messages.deny(who, "The map cannot change during a game.")
                    else
                        Arena:show(row[2])
                        Arena:send(who, "lobby")   -- the click's spawn()
                        Sidebar.refresh()
                    end
                    MapStatesMenu.open(who)   -- the old chest stayed open
                    return
                end
            end
        end,
    }
end

return MapStatesMenu
