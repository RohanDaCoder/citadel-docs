--!nonstrict
-- menus.luau — vote, profile and the admin panel.
--
-- A faithful port of the legacy Skript GUIs:
--   Commands/2_Profile.sk    (profile -> game list -> per-game stats)
--   Commands/3_AdminPanel.sk (panel -> players -> player card; timer cycle)
--   Commands/1_GameCommands.sk /changemapstate (5-row map picker)
--
-- Slot numbers are the original ones, kept so muscle memory and the old
-- layout both survive. Citadel menus are pick-only (no item moving), so
-- the Skript's "cancel event" plumbing disappears; on_pick by position
-- replaces the inventory-click handlers.
--
-- Two deliberate additions the old server lacked: the panel can start a
-- stopped system (the Skript needed a server restart), and every menu
-- opens with the click sound the map picker played.

local arena = require("arena")
local core = require("core")

local menus = {}

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

-- The old icons (0_Variables.sk): named, bold, with glint, item flags
-- hidden. Citadel item tables give us name/lore/glint directly.
local function game_icon(g)
    return {
        item = g.icon or "paper",
        name = { { g.name, color = g.title_color or "yellow", bold = true } },
        glint = true,
    }
end

function menus.is_admin(p)
    if p:has("onix.admin") then return true end
    return citadel.env == "development"
end

-- ---- vote ----------------------------------------------------------------

function menus.vote(p)
    local items = {}
    for _, name in core.order do
        local g = core.games[name]
        local votes = core.vote_count(name)
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
            local name = core.order[n]
            if name then core.cast_vote(who, name) end
            menus.vote(who)
        end,
    }
end

-- ---- profile: main -> game list -> game stat -----------------------------

-- Slot 15 of the main page opens the game list, exactly as the Skript
-- laid it out (10 stats, 13 head, 15 game statistics, 16 close).
function menus.profile(viewer, target)
    local uuid = target.uuid
    local played = core.stat(uuid, "played")
    local wins = core.stat(uuid, "wins")
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
                menus.game_list(who, target)
            end
        end,
    }
end

function menus.game_list(viewer, target)
    local uuid = target.uuid
    local items = {}

    -- The Skript walked slots from 10, skipping 13 (the head column);
    -- every registered game, votable or not, so all four have a card.
    local slot = 10
    for _, name in core.all_games() do
        local g = core.games[name]
        if slot == 13 then slot = slot + 1 end
        local played = core.stat(uuid, "played." .. g.key)
        local wins = core.stat(uuid, "wins." .. g.key)
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
                menus.profile(who, target)
                return
            end
            -- Re-derive which game landed on the picked slot.
            local slot = 10
            for _, name in core.all_games() do
                if slot == 13 then slot = slot + 1 end
                if slot == n then
                    menus.game_stat(who, target, core.games[name])
                    return
                end
                slot = slot + 1
            end
        end,
    }
end

function menus.game_stat(viewer, target, g)
    local uuid = target.uuid
    local played = core.stat(uuid, "played." .. g.key)
    local wins = core.stat(uuid, "wins." .. g.key)

    local items = {}
    items[10] = { item = "book", name = "Games Played", lore = { tostring(played) } }
    items[12] = { item = "diamond", name = "Wins", lore = { tostring(wins) } }
    items[13] = {
        item = g.icon or "paper",
        name = { { g.name, color = "aqua", bold = true } },
        glint = true,
    }

    -- The per-game extra: blocks broken for TNT Run, potato touches for
    -- Hot Potato (the stat the old profile read but never counted).
    if g.key == "tntrun" then
        items[14] = { item = "tnt", name = "Blocks Broken", lore = { tostring(core.stat(uuid, "tntrun")) } }
    elseif g.key == "hotpotato" then
        items[14] = { item = "blaze_powder", name = "Potato Touches", lore = { tostring(core.stat(uuid, "hotpotato_touches")) } }
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
                menus.game_list(who, target)
            end
        end,
    }
end

-- ---- admin panel ----------------------------------------------------------

-- The timer button cycles 5 -> 10 -> 15 -> 30 -> 60 -> 5, as the Skript's
-- ladder ran it (>= thresholds, wrapping from 60 back to 5).
local TIMER_LADDER = { 5, 10, 15, 30, 60 }

local function next_timer(t)
    for i, step in TIMER_LADDER do
        if t < step then return step end
    end
    return 5
end

function menus.admin(p)
    if not menus.is_admin(p) then
        core.deny(p, "You do not have permission.")
        return
    end

    local s = core.S
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
                menus.admin(who)
            elseif n == 11 then
                -- The old button only skipped the vote; a stopped system
                -- can also be started again from here.
                if not core.S.running then
                    core.start()
                    core.tell(who, "System started.", "green")
                elseif not core.skip_vote(who) then
                    core.deny(who, "Server is in " .. core.S.phase .. " state.")
                end
                menus.admin(who)
            elseif n == 12 then
                if not core.stop() then
                    core.deny(who, "System is already disabled!")
                end
            elseif n == 13 then
                if core.S.phase == "Ingame" then
                    core.deny(who, "Map state cannot be changed while a game is in progress!")
                else
                    menus.map_states(who)
                end
            elseif n == 14 then
                core.set_timer(next_timer(math.max(core.S.timer, 0)))
                menus.admin(who)
            elseif n == 15 then
                menus.players(who)
            elseif n == 16 then
                menus.announce(who)
            end
        end,
    }
end

function menus.players(p)
    -- The old 4-row grid: heads in the classic slots, back at 31.
    local slots = { 10, 11, 12, 13, 14, 15, 16, 19, 20, 21, 23, 24, 25, 28, 29, 30, 32, 33, 34 }
    local items = {}

    for i, target in core.S.roster do
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
                menus.admin(who)
                return
            end
            for i, slot in slots do
                if slot == n then
                    local target = core.S.roster[i]
                    if target then menus.player_card(who, target) end
                    return
                end
            end
        end,
    }
end

function menus.player_card(p, target)
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
                menus.profile(who, target)
            elseif n == 15 then
                if core.eliminate(target) then
                    core.tell(who, target.name .. " eliminated.", "yellow")
                else
                    core.deny(who, "That player is not in a round.")
                end
                menus.players(who)
            elseif n == 22 then
                menus.players(who)
            end
        end,
    }
end

function menus.announce(p)
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
                core.discord_broadcast()
                sound.play("entity.experience_orb.pickup", { volume = 0.5, pitch = 1 })
            elseif n == 15 then
                core.announce_votes()
            elseif n == 22 then
                menus.admin(who)
            end
        end,
    }
end

-- ---- map states -----------------------------------------------------------

-- /changemapstate's 5-row picker, the live server's own items in its own
-- slots: the glinted beacon/shovel/TNT/head/potato with "Click to change
-- map state to <name>" lore, three barriers where the next games will go,
-- and nothing else (no Close: the Skript had none, and Escape closes).
local STATE_ITEMS = {
    { 10, "lobby", "Lobby", "aqua", "beacon" },
    { 12, "spleef", "Spleef", "yellow", "golden_shovel" },
    { 14, "tntrun", "TNT Run", "red", "tnt" },
    { 16, "sumo", "Sumo", "dark_red", "player_head" },
    { 28, "hotpotato", "Hot Potato", "gold", "baked_potato" },
}

function menus.map_states(p)
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

    open_sound(p)   -- ui.button.click 0.5/1.2, as the old GUI's opener
    p.ui.menu{
        title = { { "Select Map State", color = "yellow", bold = true } },
        items = pad(items, 5),
        on_pick = function(who, n)
            for _, row in STATE_ITEMS do
                if row[1] == n then
                    if core.S.phase == "Ingame" then
                        -- this port's guard: the Skript would have pasted
                        -- a map straight under a running round
                        core.deny(who, "The map cannot change during a game.")
                    else
                        arena.show(row[2])
                        arena.send(who, "lobby")   -- the click's spawn()
                        core.refresh()
                    end
                    menus.map_states(who)   -- the old chest stayed open
                    return
                end
            end
        end,
    }
end

return menus
