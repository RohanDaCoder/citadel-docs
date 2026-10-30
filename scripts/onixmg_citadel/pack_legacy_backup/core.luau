--!nonstrict
-- core.luau — round cycle, votes, roster, stats and the sidebar.
--
-- A 1:1 Citadel port of the live Paper server's Skript core:
--   Core/0_Variables.sk  (prefixes, permissions, the two votable games)
--   Core/1_CoreSystem.sk (cycle, votes, rounds, elimination)
-- downloaded from plugins/Skript/scripts on 2026-10-30.
--
-- Every message is the live server's own, colour for colour:
--   prefix  "<#7A8BFA><b>Onix<#204352><b>MG <#555555>|"  (Citadel runs)
--   debug   "<#aa0000><b>ᴅᴇʙᴜɢ <#555555>|"
-- Skript's "volume 10" is Citadel's full volume (1).
--
-- Deliberate deviations, each noted because the Skript was broken:
--   * the Skript's on-disconnect handler passed an unset variable, so a
--     quitter was never removed; here leaving runs the full elimination
--   * the hot-potato "while timer <= 0" loop could never run, so the
--     potato was taken back the moment it was given; games/hotpotato.luau
--     plays the intended fuse
--   * the Skript's /startgame could extend a nearly-finished vote; here a
--     skip never adds time

local arena = require("arena")

local core = {}

core.games = {}   -- every registered game, by name
core.order = {}   -- the votable list, as 0_Variables.sk filled it

-- The old prefix, as exact Citadel colour runs.
local ONIX = color(0x7A / 255, 0x8B / 255, 0xFA / 255)
local MG = color(0x20 / 255, 0x43 / 255, 0x52 / 255)
local DEBUG_RED = color(0xAA / 255, 0, 0)

core.ACCENT = "aqua"
core.DISCORD = "discord.gg/RyKjZ2pdw2"
core.VOTE_SECONDS = 30
core.ROUND_SECONDS = 120      -- mg_start_game's one timer, every game

local RESULT_HOLD = 3         -- winner title before "Returning to lobby..."
local RESULT_RETURN = 7       -- map is lobby; players settle at spawn
local RESULT_GAP = 3          -- "The game has ended!" before the next cycle

local S = {
    phase = "Disabled",  -- Loading | Lobby | Ingame | Result | Disabled
    active = nil,
    timer = 0,
    timer_override = nil,  -- /settimer and the panel's clock land here;
                            -- the countdown loops consume it as the new
                            -- remaining time, as the Skript's direct
                            -- variable write did
    roster = {},
    votes = {},
    voted = {},
    gen = 0,
    running = false,
    skip = false,
    cycle_waiter = nil,  -- the coroutine parked in Loading when the
                         -- server is empty; resumed by on_join (a player
                         -- joined) or by core.stop (gen bumped), so the
                         -- loop never polls and never strands
}
core.S = S

-- ---- messages -------------------------------------------------------------

local function prefix_runs()
    return {
        { "Onix", color = ONIX, bold = true },
        { "MG", color = MG, bold = true },
        { " | ", color = "dark_gray" },
    }
end

-- sendDebug's prefix: "<#aa0000><b>ᴅᴇʙᴜɢ <#555555>|<reset>"
local function debug_prefix_runs()
    return {
        { "ᴅᴇʙᴜɢ", color = DEBUG_RED, bold = true },
        { " | ", color = "dark_gray" },
    }
end

--- Join two run lists into one text (Luau has no `..` for tables).
local function cat(a, b)
    local out = {}
    for _, run in a do table.insert(out, run) end
    for _, run in b do table.insert(out, run) end
    return out
end

function core.tell(p, body, color)
    p:message(cat(prefix_runs(), { { body, color = color or "white" } }))
end

function core.broadcast(body, color)
    message(cat(prefix_runs(), { { body, color = color or "white" } }))
end

--- The prefix + already-built runs: for two-tone messages such as
--- "&eSelected Game: &a&lSpleef".
function core.broadcast_runs(runs)
    message(cat(prefix_runs(), runs))
end

function core.debug(body)
    for _, p in players.list() do
        if p:has("onix.debug") then
            p:message(cat(debug_prefix_runs(), { { body, color = "white" } }))
        end
    end
end

-- The old anvil-and-pling pair. Skript's "volume 10" was its own loudness
-- trick; Citadel's volume 1 is full volume, so that is what these use.
local function deny_sound(p)
    p:sound("block.anvil.land", { volume = 1, pitch = 1 })
end

function core.deny(p, body)
    core.tell(p, body, "red")
    deny_sound(p)
end

function core.deny_runs(p, runs)
    p:message(cat(prefix_runs(), runs))
    deny_sound(p)
end

-- The Discord line (Utils/2_Discord.sk): green text, blue underlined
-- link. Citadel chat cannot open URLs, so the address is the message.
-- With a player, just to them; without, to everyone.
function core.discord_broadcast(p)
    local text = {
        { "Join our discord server! ", color = "green" },
        { core.DISCORD, color = "blue", underline = true },
    }
    if p then p:message(text) else message(text) end
end

-- ---- stats ----------------------------------------------------------------

function core.stat(uuid, key)
    return storage.get("stats." .. uuid .. "." .. key) or 0
end

function core.bump(uuid, key)
    storage.set("stats." .. uuid .. "." .. key, core.stat(uuid, key) + 1)
end

-- ---- games ----------------------------------------------------------------

--- core.order is the votable list exactly as 0_Variables.sk built it:
--- "Spleef" and "TNT Run" (Sumo and Hot Potato stayed commented out on the
--- live server). Register them anyway with votable = false and flip that
--- flag to widen the vote.
function core.register(game)
    core.games[game.name] = game
    if game.votable ~= false then
        table.insert(core.order, game.name)
    end
end

--- Every registered game, votable or not, in registration order.
function core.all_games()
    local out = {}
    for _, name in { "Spleef", "TNT Run", "Sumo", "Hot Potato" } do
        if core.games[name] then table.insert(out, name) end
    end
    return out
end

-- ---- votes ----------------------------------------------------------------

function core.vote_count(name)
    return S.votes[name] or 0
end

function core.reset_votes()
    S.votes = {}
    S.voted = {}
end

-- mg_broadcast_vote: the whole list, with a plain [VOTE] token where the
-- live MiniMessage made it clickable (Citadel chat cannot run commands;
-- the vote compass and /vote cover it).
function core.announce_votes()
    message("")
    message({ { "VOTE FOR THE NEXT MINIGAME!", color = "gold", bold = true } })
    for _, name in core.order do
        message({
            { "[VOTE]", color = "green", bold = true },
            { " ", color = "white" },
            { name, color = "white" },
            { " (" .. core.vote_count(name) .. " votes)", color = "gray" },
        })
    end
    message({
        { "Use ", color = "gray" },
        { "/vote", color = "yellow" },
        { " or click ", color = "gray" },
        { "[VOTE]", color = "green", bold = true },
    })
    message("")
end

function core.cast_vote(p, name)
    if S.phase ~= "Lobby" then
        core.deny(p, "No voting in progress!")
        return false
    end
    if S.voted[p] then
        core.deny(p, "You already voted!")
        return false
    end
    if not core.games[name] or not table.find(core.order, name) then
        core.deny(p, "Invalid game!")
        return false
    end

    S.voted[p] = true
    S.votes[name] = core.vote_count(name) + 1

    core.announce_votes()
    p:message(cat(prefix_runs(), {
        { "You voted for ", color = "green" },
        { name, color = "white" },
        { "!", color = "green" },
    }))
    core.debug(p.name .. " voted for " .. name)
    p:sound("block.note_block.pling", { volume = 1, pitch = 2 })
    core.refresh()
    return true
end

--- mg_finalize_vote: the highest count wins, the first game in list order
--- taking ties; with no votes at all a random pick is announced.
--- Returns the game and whether any votes were cast.
function core.winning_vote()
    local best, bestn = nil, -1
    for _, name in core.order do
        local n = core.vote_count(name)
        if n > bestn then
            best, bestn = name, n
        end
    end
    if bestn <= 0 then
        best = core.order[math.random(#core.order)]
        core.broadcast_runs({
            { "No votes cast! Randomly picking ", color = "yellow" },
            { best, color = "green", bold = true },
        })
        return best, false
    end
    return best, true
end

-- ---- roster ---------------------------------------------------------------

function core.in_roster(p)
    for _, v in S.roster do
        if v == p then return true end
    end
    return false
end

function core.leave_roster(p)
    for i, v in S.roster do
        if v == p then
            table.remove(S.roster, i)
            return true
        end
    end
    return false
end

--- The old spawn(): the lobby point, wherever the current map puts it.
function core.lobby(p)
    p.gamemode = 2
    p.health = 20
    arena.send(p, "lobby")
    core.set_lobby_hotbar(p)
end

--- mg_eliminate: out of the round, back to the lobby point, with the
--- lava sound the old server played for everyone. `gone` skips the
--- teleport half for a player who just left.
function core.eliminate(p, gone)
    if S.phase ~= "Ingame" then return false end
    if not core.leave_roster(p) then return false end

    core.broadcast_runs({
        { p.name, color = "yellow" },
        { " was eliminated from the game!", color = "red" },
    })
    if not gone then
        if S.active == "TNT Run" then
            p:message({
                { "Blocks Broken: ", color = "gray" },
                { tostring(core.stat(p.uuid, "tntrun")), color = "yellow" },
            })
        end
        core.lobby(p)
    end
    sound.play("block.lava.extinguish", { volume = 1, pitch = 1 })
    return true
end

-- ---- sidebar and hotbar ---------------------------------------------------
-- The sidebar itself is an addition: the Skript had none, it shows nothing
-- the chat did not, and it keeps the vote readable without clickable chat.

local function phase_label()
    if S.phase == "Lobby" then return "Voting" end
    if S.phase == "Ingame" then return "Playing" end
    if S.phase == "Result" then return "Results" end
    if S.phase == "Loading" then return "Loading" end
    return S.phase
end

function core.refresh()
    local lines = {
        { { "State   ", color = "gray" }, { phase_label(), color = "white" } },
        { { "Game    ", color = "gray" }, { S.active or "-", color = "white" } },
        { { "Timer   ", color = "gray" }, { tostring(math.max(S.timer, 0)) .. "s", color = "yellow" } },
        { { "Alive   ", color = "gray" }, { tostring(#S.roster), color = "white" } },
        "",
    }
    if S.phase == "Lobby" then
        for _, name in core.order do
            table.insert(lines, {
                { name, color = "white" },
                { "  " .. core.vote_count(name), color = "green" },
            })
        end
        table.insert(lines, "")
        table.insert(lines, { { "/vote <game>", color = "yellow" } })
    end
    ui.sidebar{ title = { "ONIX MINIGAMES", color = core.ACCENT, bold = true }, lines = lines }
end

function core.set_lobby_hotbar(p)
    p:hotbar{
        [1] = { item = "compass", name = "Vote", lore = { "Choose the next game" } },
        [2] = { item = "book", name = "Profile", lore = { "Your stats" } },
        [5] = { item = "paper", name = "Discord", lore = { core.DISCORD } },
    }
end

function core.on_join(p)
    -- The Skript only ran spawn() on join; the gold welcome block that
    -- follows is the live server's Essentials motd, sent by main.luau.
    core.lobby(p)
    core.refresh()
    -- If the cycle loop is parked in Loading waiting for the first
    -- player, this join is its sole wake-up. Resume on the next
    -- scheduler tick so on_join itself stays non-blocking.
    local waiter = S.cycle_waiter
    if waiter and coroutine.status(waiter) == "suspended" then
        S.cycle_waiter = nil
        task.spawn(function() coroutine.resume(waiter) end)
    end
end

-- ---- one round ------------------------------------------------------------

function core.play(name, gen)
    local g = core.games[name]
    if not g then return end

    S.phase = "Ingame"
    S.active = name
    S.roster = {}

    sound.play("entity.player.levelup", { volume = 1, pitch = 1 })
    ui.title{ title = "", subtitle = "Loading...", color = "gray", stay = 2 }

    -- Everyone playing is rostered, counted and sent to the lobby point
    -- first, exactly as mg_start_game's spawn() loop did, adventure mode
    -- included.
    for _, p in players.list() do
        table.insert(S.roster, p)
        p.gamemode = 2
        p.health = 20
        arena.send(p, "lobby")
        core.bump(p.uuid, "played")
        core.bump(p.uuid, "played." .. g.key)
    end

    arena.show(g.arena)
    task.wait(3)

    -- "&e&lSpleef &8- &fDig your way to victory!" — a plain broadcast, no
    -- prefix, each game in its own colour, as mg_start_game sent them.
    message({
        { name, color = g.title_color or "yellow", bold = true },
        { " - ", color = "dark_gray" },
        { g.blurb or "", color = "white" },
    })
    local spawn = arena.spawn(g.arena)
    local yaw = arena.yaw(g.arena)
    for _, p in S.roster do
        p:teleport(spawn, { yaw = yaw, pitch = 0 })
    end

    if g.start then g.start() end

    local remaining = g.duration or core.ROUND_SECONDS
    local acc = 0
    S.timer = math.ceil(remaining)
    core.refresh()

    -- The round ends on time, or as soon as one player is left standing
    -- (mg_eliminate ended the game at roster size 0 or 1). The void check
    -- is the per-game "on player move: y < -48", and only the games that
    -- had one carry it.
    while S.gen == gen and remaining > 0 and #S.roster > 1 do
        if S.timer_override then
            remaining = S.timer_override
            S.timer_override = nil
        end
        local dt = task.wait(0.05)
        remaining = remaining - dt

        if g.step then g.step(dt) end

        if g.void_y then
            for i = #S.roster, 1, -1 do
                local p = S.roster[i]
                local at = p.at
                if at and at.y < g.void_y then core.eliminate(p) end
            end
        end

        acc = acc + dt
        if acc >= 0.25 then
            acc = 0
            S.timer = math.max(math.ceil(remaining), 0)
            core.refresh()
            ui.actionbar({
                { "Active: ", color = "yellow" },
                { name, color = "green" },
                { " | ", color = "dark_gray" },
                { "Remaining: ", color = "yellow" },
                { S.timer .. "s", color = "white" },
            })
        end
    end

    if g.stop then g.stop() end
end

function core.finish(gen)
    S.phase = "Result"
    S.timer = 10

    -- mg_end_game: nobody left is "&8[&7Nobody&8]"; anyone left is the
    -- first player of the list in order (the Skript's later "random
    -- element" branch was dead code — its guard could never fire).
    local winner = nil
    if #S.roster > 0 then
        winner = S.roster[1]
    end

    local name_runs
    if winner then
        name_runs = { { winner.name, color = "green" } }
    else
        name_runs = {
            { "[", color = "dark_gray" },
            { "Nobody", color = "gray" },
            { "]", color = "dark_gray" },
        }
    end

    if winner then
        local g = core.games[S.active]
        core.bump(winner.uuid, "wins")
        if g then core.bump(winner.uuid, "wins." .. g.key) end
    end

    core.broadcast_runs(cat(name_runs, { { " is The Winner", color = "yellow" } }))
    ui.title{
        title = { "WINNER!", color = "yellow", bold = true },
        subtitle = cat(name_runs, { { " won the game!", color = "yellow" } }),
        stay = 5,
    }
    sound.play("ui.toast.challenge_complete", { volume = 1, pitch = 1 })

    task.wait(RESULT_HOLD)

    core.broadcast("Returning to lobby...", "gray")
    arena.show("lobby")
    task.wait(RESULT_RETURN)

    S.roster = {}
    S.active = nil
    for _, p in players.list() do
        core.lobby(p)
    end

    if S.gen ~= gen then return end

    -- {minigames::system::enabled} guard first, then the closing pair.
    core.broadcast_runs({ { "The game has ended!", color = "red", bold = true } })
    message("")
    task.wait(RESULT_GAP)
end

-- ---- cycle ----------------------------------------------------------------

function core.run()
    S.gen = S.gen + 1
    local gen = S.gen
    S.running = true

    while S.gen == gen do
        -- Loading: park on the player-join event when the server is
        -- empty, instead of polling every five seconds. The only way
        -- players.count() can rise above zero is a join, so on_join is
        -- the sole wake-up we need; core.stop bumps gen and resumes us
        -- too, so a shutdown while empty does not strand the loop. A
        -- task-spawn'd thread suspended via coroutine.yield is not
        -- scheduler-resumed, so this is a true wait, not a spin.
        S.phase = "Loading"
        S.active = nil
        S.roster = {}
        S.timer = 0
        core.refresh()
        if players.count() == 0 and S.gen == gen then
            citadel.log("No players to start cycle - waiting for a player to join.")
            S.cycle_waiter = coroutine.running()
            coroutine.yield()
            S.cycle_waiter = nil
        end
        if S.gen ~= gen then break end
        core.debug("Starting new cycle...")

        S.phase = "Lobby"
        S.skip = false
        core.reset_votes()
        arena.show("lobby")
        for _, p in players.list() do core.lobby(p) end

        -- The vote: 30 s, the list read out at 30/20/10, a note every
        -- one of the last five seconds, exactly as mg_start_cycle ran it.
        local remaining = core.VOTE_SECONDS
        local shown = -1
        local last_tick = -1
        while remaining > 0 and S.gen == gen do
            if S.timer_override then
                remaining = S.timer_override
                S.timer_override = nil
                shown = -1
            end
            if S.skip then
                S.skip = false
                remaining = math.min(remaining, 5)
            end
            S.timer = math.ceil(remaining)
            if S.timer ~= shown then
                shown = S.timer
                if S.timer == core.VOTE_SECONDS or S.timer == 20 or S.timer == 10 then
                    core.announce_votes()
                end
                core.refresh()
            end
            if S.timer ~= last_tick then
                last_tick = S.timer
                if S.timer <= 5 then
                    sound.play("block.note_block.bit", { volume = 1, pitch = 1 })
                end
            end
            -- "&bVoting Phase &8| &eNext game in: &f%timer%s", then
            -- "&6&lSTARTING IN &f&l%timer%s" for the last five seconds.
            if S.timer <= 5 then
                ui.actionbar({
                    { "STARTING IN ", color = "gold", bold = true },
                    { S.timer .. "s", color = "white", bold = true },
                })
            else
                ui.actionbar({
                    { "Voting Phase ", color = "aqua" },
                    { "| ", color = "dark_gray" },
                    { "Next game in: ", color = "yellow" },
                    { S.timer .. "s", color = "white" },
                })
            end
            remaining = remaining - task.wait(0.5)
        end

        if S.gen ~= gen then break end

        local name, had_votes = core.winning_vote()
        if had_votes then
            core.broadcast_runs({
                { "Selected Game: ", color = "yellow" },
                { name, color = "green", bold = true },
            })
        end
        task.wait(2)
        if S.gen ~= gen then break end

        core.play(name, gen)
        if S.gen ~= gen then break end
        core.finish(gen)
    end

    S.running = false
    core.refresh()
end

-- ---- controls -------------------------------------------------------------

-- /startgame: the old command cut the vote to five seconds, played the
-- bass note and named who skipped.
function core.skip_vote(p)
    if S.phase ~= "Lobby" then return false end
    if S.timer <= 5 then return false end
    S.skip = true
    sound.play("block.note_block.bass", { volume = 1, pitch = 1 })
    core.broadcast_runs({
        { (p and p.name or "Someone"), color = "yellow" },
        { " skipped waiting time.", color = "gray" },
    })
    return true
end

-- /settimer <seconds>: the old command wrote the variable and only the
-- debug line ever said so.
function core.set_timer(n, who)
    if n and n > 0 then
        S.timer = math.floor(n)
        S.timer_override = math.floor(n)
        core.debug("Admin " .. (who and who.name or "?") .. " set timer to " .. S.timer .. " seconds")
        core.refresh()
    end
end

function core.stop()
    if not S.running then return false end
    S.gen = S.gen + 1
    -- If the run loop is parked in Loading on the join event, bumping
    -- gen alone cannot wake it (coroutine.yield is not scheduler-resumed);
    -- resume it so the loop sees the new gen, exits and clears S.running.
    local waiter = S.cycle_waiter
    if waiter then
        S.cycle_waiter = nil
        task.spawn(function()
            if coroutine.status(waiter) == "suspended" then coroutine.resume(waiter) end
        end)
    end
    S.phase = "Disabled"
    S.active = nil
    S.roster = {}
    S.timer = 0
    core.reset_votes()
    arena.show("lobby")
    for _, p in players.list() do core.lobby(p) end
    ui.sidebar(false)
    ui.actionbar("")
    sound.play("block.note_block.bass", { volume = 1, pitch = 1 })
    core.broadcast("System shutdown!", "gray")
    return true
end

function core.start()
    if S.running then return false end
    S.phase = "Loading"
    task.spawn(core.run)
    return true
end

return core
