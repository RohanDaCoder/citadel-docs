--!nonstrict
-- ui/menus/AdminMenu.luau
-- One purpose: the admin panel — system status, start/stop, the map
-- picker link, the timer ladder (5 -> 10 -> 15 -> 30 -> 60 -> 5), the
-- players submenu and the announcements submenu.

local state = require("core/GameState")
local Messages = require("core/Messages")
local CycleControls = require("core/CycleControls")
local Perms = require("util/Perms")
local kit = require("ui/MenuKit")
local PlayersMenu = require("ui/menus/PlayersMenu")
local AnnounceMenu = require("ui/menus/AnnounceMenu")
local MapStatesMenu = require("ui/menus/MapStatesMenu")

local AdminMenu = {}

local TIMER_LADDER = { 5, 10, 15, 30, 60 }

local function next_timer(t)
    for _, step in TIMER_LADDER do
        if t < step then return step end
    end
    return 5
end

function AdminMenu.open(p)
    if not Perms.is_admin(p) then
        Messages.deny(p, "You do not have permission.")
        return
    end

    local s = state

    local items = {}
    items[10] = {
        item = "beacon",
        name = { { "System Status", color = "aqua", bold = true } },
        lore = {
            { { "State: ", color = "gray" }, { s.phase, color = "white" } },
            { { "Active: ", color = "gray" }, { s.active or "None", color = "white" } },
            { { "Timer: ", color = "gray" }, { math.max(s.timer, 0) .. "s", color = "white" } },
            { { "In round: ", color = "gray" }, { tostring(#s.roster), color = "white" } },
            { { "Players: ", color = "gray" }, { players.count(), color = "white" } },
            "Click to refresh",
        },
        glint = true,
    }
    items[11] = { item = "emerald", name = { { "Start Game", color = "green", bold = true } }, lore = { "Start the game if in Lobby" } }
    items[12] = { item = "redstone_block", name = { { "Stop Game", color = "red", bold = true } }, lore = { "Force stop the current game" } }
    items[13] = {
        item = "filled_map",
        name = { { "Change Map", color = "white", bold = true } },
        glint = true,
        lore = s.phase == "Ingame"
            and { "[DISABLED FOR STATE INGAME]" }
            or { "Change the map state" },
    }
    items[14] = {
        item = "clock",
        name = { { "Timer: ", color = "yellow", bold = true }, { math.max(s.timer, 0) .. "s", color = "white", bold = true } },
        lore = { "Click to cycle: 5s, 10s, 15s, 30s, 60s" },
    }
    items[15] = {
        item = "player_head",
        name = { { "Players (", color = "aqua", bold = true }, { tostring(#s.roster), color = "white", bold = true }, { ")", color = "aqua", bold = true } },
        lore = { "Manage active players" },
    }
    items[16] = { item = "goat_horn", name = { { "Announcements", color = "yellow", bold = true } }, glint = true, lore = { "Announcements and voting" } }
    items[22] = kit.close_item("Close the admin panel")

    kit.open_sound(p)
    p.ui.menu{
        title = { { "Admin Panel", color = "gray", bold = true } },
        items = kit.pad(items, 3),
        on_pick = function(who, n)
            if n == 10 then
                AdminMenu.open(who)
            elseif n == 11 then
                if not state.running then
                    CycleControls:start()
                    Messages.tell(who, "System started.", "green")
                elseif not CycleControls:skipVote(who) then
                    Messages.deny(who, "Server is in " .. state.phase .. " state.")
                end
                AdminMenu.open(who)
            elseif n == 12 then
                if not CycleControls:stop() then
                    Messages.deny(who, "System is already disabled!")
                end
            elseif n == 13 then
                if state.phase == "Ingame" then
                    Messages.deny(who, "Map state cannot be changed while a game is in progress!")
                else
                    MapStatesMenu.open(who)
                end
            elseif n == 14 then
                CycleControls:setTimer(next_timer(math.max(state.timer, 0)))
                AdminMenu.open(who)
            elseif n == 15 then
                PlayersMenu.open(who)
            elseif n == 16 then
                AnnounceMenu.open(who)
            end
        end,
    }
end

return AdminMenu
