--!nonstrict
-- ui/menus/MapStatesMenu.luau
-- One purpose: the map-state picker — the live server's own chest, item
-- for item and slot for slot: 5 rows, the four states spaced across the
-- second row, Hot Potato and the three "to be added" barriers across the
-- fourth, no Back (Escape closes; the old chest stayed open, so it
-- re-opens after every pick). The Skript's slots are 0-based, so every
-- one is +1 here — the exact-slot content entries keep the layout while
-- the kit handles the padding, the size and the pick dispatch.

local state = require("core/GameState")
local Arena = require("core/Arena")
local Messages = require("core/Messages")
local Sidebar = require("ui/Sidebar")
local kit = require("ui/MenuKit")

local MapStatesMenu = {}

-- Skript slots 10/12/14/16 (second row) and 28 (fourth row), 0-based.
local STATES = {
    { 11, "lobby", "Lobby", "aqua", "beacon" },
    { 13, "spleef", "Spleef", "yellow", "golden_shovel" },
    { 15, "tntrun", "TNT Run", "red", "tnt" },
    { 17, "sumo", "Sumo", "dark_red", "player_head" },
    { 29, "hotpotato", "Hot Potato", "gold", "baked_potato" },
}

-- Skript slots 30/32/34, 0-based: the next games' placeholders.
local SOON_SLOTS = { 31, 33, 35 }

function MapStatesMenu.open(p)
    local content = {}

    for _, row in STATES do
        local slot, key, label, colr, item = row[1], row[2], row[3], row[4], row[5]
        table.insert(content, {
            slot = slot,
            item = {
                key = key,
                item = item,
                name = { { label, color = colr, bold = true } },
                glint = true,
                lore = {
                    { { "Click to change map state to ", color = "gray" }, { label, color = "yellow" } },
                },
            },
        })
    end

    local soon = {
        item = "barrier",
        name = { { "To be added..", color = "red", bold = true } },
        lore = { { "New minigames will be added here", color = "yellow" } },
    }
    for _, slot in SOON_SLOTS do
        table.insert(content, { slot = slot, item = soon })
    end

    kit.menu(p, {
        title = { { "Select Map State", color = "yellow", bold = true } },
        rows = 5,
        content = content,
        on_pick = function(who, key)
            if state.phase == "Ingame" then
                Messages.deny(who, "The map cannot change during a game.")
            else
                Arena:show(key)
                Arena:send(who, "lobby")   -- the click's spawn()
                Sidebar.refresh()
            end
            MapStatesMenu.open(who)   -- the old chest stayed open
        end,
    })
end

return MapStatesMenu
