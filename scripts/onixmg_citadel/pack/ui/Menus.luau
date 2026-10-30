--!nonstrict
-- ui/Menus.luau
-- The vote, profile and admin menus. Slot numbers are the original ones,
-- kept so muscle memory and the old layout both survive. Citadel menus
-- are pick-only (no item moving), so on_pick by position replaces the old
-- inventory-click handlers. Every menu opens with the click sound the map
-- picker played.

local state = require("core/GameState")
local registry = require("core/GameRegistry")
local Arena = require("core/Arena")
local Messages = require("core/Messages")
local Stats = require("core/Stats")
local VoteBook = require("core/VoteBook")
local CycleDriver = require("core/CycleDriver")
local Sidebar = require("ui/Sidebar")
local Perms = require("util/Perms")

local Menus = {}

local PANE = "gray_stained_glass_pane"

local function pad(items, rows)
    local out = {}
    local n = rows * 9
    for i = 1, n do
        out[i] = items[i] or { item = PANE, name = " " }
    end
    return out
end

local function open_sound(p)
    p:sound("ui.button.click", { volume = 0.5, pitch = 1.2 })
end

-- The old icons: named, bold, with glint.
local function game_icon(g)
    return {
        item = g.icon or "paper",
        name = { { g.name, color = g.title_color or "yellow", bold = true } },
        glint = true,
    }
end

-- ---- vote ----------------------------------------------------------------

function Menus.vote(p)
    local items = {}
    for _, name in registry:votable() do
        local g = registry:get(name)
        local votes = state:vote_count(name)
        table.insert(items, {
            item = g.icon or "paper",
            name = { { name, color = g.title_color or "yellow", bold = true } },
            lore = {
                g.blurb or "",
                votes .. (votes == 1 and " vote" or " votes"),
                "Click to vote",
            },
            count = math.max(votes, 1),
            glint = true,
        })
    end

    open_sound(p)
    p.ui.menu{
        title = { { "Vote for the next game", color = "yellow", bold = true } },
        items = pad(items, 3),
        on_pick = function(who, n)
            local name = registry:votable()[n]
            if name then VoteBook.cast(who, name) end
            Menus.vote(who)
        end,
    }
end

-- ---- profile: main -> game list -> game stat -----------------------------

-- Slot 15 of the main page opens the game list, as the original layout
-- had it (10 stats, 13 head, 15 game statistics, 16 close).
function Menus.profile(viewer, target)
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
    items[16] = { item = "barrier", name = { { "Close", color = "red", bold = true } }, lore = { "Click to close" } }

    open_sound(viewer)
    viewer.ui.menu{
        title = {
            { "Profile", color = "gray", bold = true },
            { " - ", color = "gray" },
            { target.name, color = "white" },
        },
        items = pad(items, 3),
        on_pick = function(who, n)
            if n == 15 then
                Menus.game_list(who, target)
            end
        end,
    }
end

function Menus.game_list(viewer, target)
    local uuid = target.uuid
    local items = {}

    -- The original walked slots from 10, skipping 13 (the head column);
    -- every registered game, votable or not, so all four have a card.
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

    items[22] = { item = "arrow", name = { { "Back", color = "red", bold = true } }, lore = { "Return to profile" } }

    open_sound(viewer)
    viewer.ui.menu{
        title = {
            { "Game Stats", color = "gray", bold = true },
            { " - ", color = "gray" },
            { target.name, color = "white" },
        },
        items = pad(items, 3),
        on_pick = function(who, n)
            if n == 22 then
                Menus.profile(who, target)
                return
            end
            -- Re-derive which game landed on the picked slot.
            local slot = 10
            for _, name in registry:all() do
                if slot == 13 then slot = slot + 1 end
                if slot == n then
                    Menus.game_stat(who, target, registry:get(name))
                    return
                end
                slot = slot + 1
            end
        end,
    }
end

function Menus.game_stat(viewer, target, g)
    local uuid = target.uuid
    local played = Stats.stat(uuid, "played." .. g.key)
    local wins = Stats.stat(uuid, "wins." .. g.key)

    local items = {}
    items[10] = { item = "book", name = "Games Played", lore = { tostring(played) } }
    items[12] = { item = "diamond", name = "Wins", lore = { tostring(wins) } }
    items[13] = {
        item = g.icon or "paper",
        name = { { g.name, color = "aqua", bold = true } },
        glint = true,
    }

    -- The per-game extra: blocks broken for TNT Run, potato touches for
    -- Hot Potato.
    if g.key == "tntrun" then
        items[14] = { item = "tnt", name = "Blocks Broken", lore = { tostring(Stats.stat(uuid, "tntrun")) } }
    elseif g.key == "hotpotato" then
        items[14] = { item = "blaze_powder", name = "Potato Touches", lore = { tostring(Stats.stat(uuid, "hotpotato_touches")) } }
    end

    items[16] = { item = "arrow", name = { { "Back", color = "red", bold = true } }, lore = { "Return to game list" } }

    open_sound(viewer)
    viewer.ui.menu{
        title = {
            { g.name, color = "gray", bold = true },
            { " - ", color = "gray" },
            { target.name, color = "white" },
        },
        items = pad(items, 3),
        on_pick = function(who, n)
            if n == 16 then
                Menus.game_list(who, target)
            end
        end,
    }
end

-- ---- admin panel ---------------------------------------------------------

-- The timer button cycles 5 -> 10 -> 15 -> 30 -> 60 -> 5, as the original
-- ladder ran it (>= thresholds, wrapping from 60 back to 5).
local TIMER_LADDER = { 5, 10, 15, 30, 60 }

local function next_timer(t)
    for _, step in TIMER_LADDER do
        if t < step then return step end
    end
    return 5
end

function Menus.admin(p)
    if not Perms.is_admin(p) then
        Messages.deny(p, "You do not have permission.")
        return
    end

    local s = state
    local running = s.running and s.phase ~= "Disabled"

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
    items[22] = { item = "barrier", name = { { "Close", color = "red", bold = true } }, lore = { "Close the admin panel" } }

    open_sound(p)
    p.ui.menu{
        title = { { "Admin Panel", color = "gray", bold = true } },
        items = pad(items, 3),
        on_pick = function(who, n)
            if n == 10 then
                Menus.admin(who)
            elseif n == 11 then
                if not state.running then
                    CycleDriver:start()
                    Messages.tell(who, "System started.", "green")
                elseif not CycleDriver:skipVote(who) then
                    Messages.deny(who, "Server is in " .. state.phase .. " state.")
                end
                Menus.admin(who)
            elseif n == 12 then
                if not CycleDriver:stop() then
                    Messages.deny(who, "System is already disabled!")
                end
            elseif n == 13 then
                if state.phase == "Ingame" then
                    Messages.deny(who, "Map state cannot be changed while a game is in progress!")
                else
                    Menus.map_states(who)
                end
            elseif n == 14 then
                CycleDriver:setTimer(next_timer(math.max(state.timer, 0)))
                Menus.admin(who)
            elseif n == 15 then
                Menus.players(who)
            elseif n == 16 then
                Menus.announce(who)
            end
        end,
    }
end

function Menus.players(p)
    -- The old 4-row grid: heads in the classic slots, back at 31.
    local slots = { 10, 11, 12, 13, 14, 15, 16, 19, 20, 21, 23, 24, 25, 28, 29, 30, 32, 33, 34 }
    local items = {}

    for i, target in state.roster do
        local slot = slots[i]
        if not slot then break end
        items[slot] = {
            item = "player_head",
            skin = target.name,
            name = { { target.name, color = "aqua" } },
        }
    end

    items[31] = { item = "arrow", name = { { "Back", color = "red", bold = true } }, lore = { "Return to admin panel" } }

    open_sound(p)
    p.ui.menu{
        title = { { "Players", color = "gray", bold = true } },
        items = pad(items, 4),
        on_pick = function(who, n)
            if n == 31 then
                Menus.admin(who)
                return
            end
            for i, slot in slots do
                if slot == n then
                    local target = state.roster[i]
                    if target then Menus.player_card(who, target) end
                    return
                end
            end
        end,
    }
end

function Menus.player_card(p, target)
    local items = {}
    items[11] = { item = "book", name = { { "View Profile", color = "aqua", bold = true } }, lore = { "View " .. target.name .. "'s profile" } }
    items[13] = {
        item = "player_head",
        skin = target.name,
        name = { { target.name, color = "aqua" } },
    }
    items[15] = { item = "barrier", name = { { "Eliminate", color = "red", bold = true } }, lore = { "Remove " .. target.name .. " from the game" } }
    items[22] = { item = "arrow", name = { { "Back", color = "red", bold = true } }, lore = { "Return to player list" } }

    open_sound(p)
    p.ui.menu{
        title = { { target.name, color = "gray", bold = true } },
        items = pad(items, 3),
        on_pick = function(who, n)
            if n == 11 then
                Menus.profile(who, target)
            elseif n == 15 then
                if CycleDriver:eliminate(target) then
                    Messages.tell(who, target.name .. " eliminated.", "yellow")
                else
                    Messages.deny(who, "That player is not in a round.")
                end
                Menus.players(who)
            elseif n == 22 then
                Menus.players(who)
            end
        end,
    }
end

function Menus.announce(p)
    local items = {}
    items[11] = { item = "blue_wool", name = { { "Discord", color = "blue", bold = true } }, lore = { "Broadcast the Discord link to all players" } }
    items[13] = { item = "goat_horn", name = { { "Announcements", color = "yellow", bold = true } }, glint = true }
    items[15] = { item = "green_wool", name = { { "Vote Menu", color = "green", bold = true } }, lore = { "Broadcast the vote menu to all players" } }
    items[22] = { item = "arrow", name = { { "Back", color = "red", bold = true } }, lore = { "Return to admin panel" } }

    open_sound(p)
    p.ui.menu{
        title = { { "Announcements", color = "gray", bold = true } },
        items = pad(items, 3),
        on_pick = function(who, n)
            if n == 11 then
                Messages.discord_broadcast()
                sound.play("entity.experience_orb.pickup", { volume = 0.5, pitch = 1 })
            elseif n == 15 then
                VoteBook.announce()
            elseif n == 22 then
                Menus.admin(who)
            end
        end,
    }
end

-- ---- map states ----------------------------------------------------------

-- /changemapstate's 5-row picker, the live server's own items in its own
-- slots: the glinted beacon/shovel/TNT/head/potato with "Click to change
-- map state to <name>" lore, three barriers where the next games will go.
local STATE_ITEMS = {
    { 10, "lobby", "Lobby", "aqua", "beacon" },
    { 12, "spleef", "Spleef", "yellow", "golden_shovel" },
    { 14, "tntrun", "TNT Run", "red", "tnt" },
    { 16, "sumo", "Sumo", "dark_red", "player_head" },
    { 28, "hotpotato", "Hot Potato", "gold", "baked_potato" },
}

function Menus.map_states(p)
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

    open_sound(p)
    p.ui.menu{
        title = { { "Select Map State", color = "yellow", bold = true } },
        items = pad(items, 5),
        on_pick = function(who, n)
            for _, row in STATE_ITEMS do
                if row[1] == n then
                    if state.phase == "Ingame" then
                        Messages.deny(who, "The map cannot change during a game.")
                    else
                        Arena:show(row[2])
                        Arena:send(who, "lobby")
                        Sidebar.refresh()
                    end
                    Menus.map_states(who)
                    return
                end
            end
        end,
    }
end

return Menus
