--!nonstrict
-- ui/menus/AdminMenu.luau
-- One purpose: the admin panel — system status, start/stop, the map
-- picker link, the timer ladder (5 -> 10 -> 15 -> 30 -> 60 -> 5), the
-- players submenu and the announcements submenu. One row of seven
-- buttons; the kit centers it and hands picks back by key.

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

    kit.menu(p, {
        title = { { "Admin Panel", color = "gray", bold = true } },
        rows = 3,
        content = {
            { items = {
                {
                    key = "status",
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
                },
                {
                    key = "start",
                    item = "emerald",
                    name = { { "Start Game", color = "green", bold = true } },
                    lore = { "Start the game if in Lobby" },
                },
                {
                    key = "stop",
                    item = "redstone_block",
                    name = { { "Stop Game", color = "red", bold = true } },
                    lore = { "Force stop the current game" },
                },
                {
                    key = "map",
                    item = "filled_map",
                    name = { { "Change Map", color = "white", bold = true } },
                    glint = true,
                    lore = s.phase == "Ingame"
                        and { "[DISABLED FOR STATE INGAME]" }
                        or { "Change the map state" },
                },
                {
                    key = "timer",
                    item = "clock",
                    name = { { "Timer: ", color = "yellow", bold = true }, { math.max(s.timer, 0) .. "s", color = "white", bold = true } },
                    lore = { "Click to cycle: 5s, 10s, 15s, 30s, 60s" },
                },
                {
                    key = "players",
                    item = "player_head",
                    name = { { "Players (", color = "aqua", bold = true }, { tostring(#s.roster), color = "white", bold = true }, { ")", color = "aqua", bold = true } },
                    lore = { "Manage active players" },
                },
                {
                    key = "announce",
                    item = "goat_horn",
                    name = { { "Announcements", color = "yellow", bold = true } },
                    glint = true,
                    lore = { "Announcements and voting" },
                },
            } },
        },
        close = "Close the admin panel",
        on_pick = function(who, key)
            if key == "status" then
                AdminMenu.open(who)
            elseif key == "start" then
                if not state.running then
                    CycleControls:start()
                    Messages.tell(who, "System started.", "green")
                elseif not CycleControls:skipVote(who) then
                    Messages.deny(who, "Server is in " .. state.phase .. " state.")
                end
                AdminMenu.open(who)
            elseif key == "stop" then
                if not CycleControls:stop() then
                    Messages.deny(who, "System is already disabled!")
                end
            elseif key == "map" then
                if state.phase == "Ingame" then
                    Messages.deny(who, "Map state cannot be changed while a game is in progress!")
                else
                    MapStatesMenu.open(who)
                end
            elseif key == "timer" then
                CycleControls:setTimer(next_timer(math.max(state.timer, 0)))
                AdminMenu.open(who)
            elseif key == "players" then
                PlayersMenu.open(who)
            elseif key == "announce" then
                AnnounceMenu.open(who)
            end
        end,
    })
end

return AdminMenu
