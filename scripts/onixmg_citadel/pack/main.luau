--!nonstrict
-- main.luau — wiring: maps, games, input, commands, announcements.
--
-- A 1:1 port of the live Paper server's Skript surface:
--   Commands/1_GameCommands.sk  (vote, startgame, stopgame, settimer,
--                                changemapstate, eliminate)
--   Utils/1_Spawn.sk            (spawn, center, join/respawn handling)
--   Utils/2_Discord.sk          (/discord + the 2-minute broadcast)
--   Games/*.sk                  (per-game input, routed through core)
-- plus the two live plugins a Citadel pack can stand in for:
--   LuckPerms + LPC   — chat renders "{prefix}{name}: {message}", with
--                       the owner's gradient small-caps tag
--   TAB               — the tab list's line/logo header and the ᴏɴʟɪɴᴇ
--                       footer, logo animating as TAB did
--   Essentials motd   — the four gold welcome lines on join
-- and /list, so the welcome's third line tells the truth.
--
-- Citadel notes:
--   * the old hotbar items came from other plugins; here the hotbar is a
--     menu (Vote compass, Profile book, Discord paper)
--   * Citadel chat cannot run commands, so the clickable [VOTE] line
--     became the vote menu and /vote
--   * /spawn keeps the Skript's 3-second cooldown, and /startgame and
--     /stopgame keep their 2-second ones

local arena = require("arena")
local core = require("core")
local menus = require("menus")

core.register(require("games/spleef"))
core.register(require("games/tntrun"))
core.register(require("games/sumo"))
core.register(require("games/hotpotato"))

arena.install()
arena.show("lobby")

citadel.log("[onixmg] maps: " .. table.concat(arena.maps(), ", "))
citadel.log("[onixmg] lobby spawn: " .. tostring(arena.spawn("lobby")))

-- ---- the live server's cosmetics ------------------------------------------

-- LuckPerms' owner tag, letter for letter:
-- "&r&8[&#cf0ab9&lᴏ&#d71ea3&lᴡ&#e0328e&lɴ&#e84678&lᴇ&#f05a62&lʀ&8] &r"
local function owner_tag()
    return {
        { "[", color = "dark_gray" },
        { "ᴏ", color = color(207 / 255, 10 / 255, 185 / 255), bold = true },
        { "ᴡ", color = color(215 / 255, 30 / 255, 163 / 255), bold = true },
        { "ɴ", color = color(224 / 255, 50 / 255, 142 / 255), bold = true },
        { "ᴇ", color = color(232 / 255, 70 / 255, 120 / 255), bold = true },
        { "ʀ", color = color(240 / 255, 90 / 255, 98 / 255), bold = true },
        { "] ", color = "dark_gray" },
    }
end

-- LPC's chat-format: "{prefix}{name}&r: {message}", the prefix being the
-- player's LuckPerms group tag (the owner's gradient tag; the default
-- group never had one). The default rendering is replaced: return false.
players.on_chat(function(p, text)
    local runs = {}
    if menus.is_admin(p) then
        for _, run in owner_tag() do table.insert(runs, run) end
    end
    table.insert(runs, { p.name })
    table.insert(runs, { ": " })
    table.insert(runs, { text })
    message(runs)
    return false
end)

-- TAB's header/footer. The logo is the animation's two frames, held in
-- the exact per-letter colours the live server cycled; the line is the
-- yellow gradient of underscores; the footer keeps the ᴏɴʟɪɴᴇ line (the
-- tps and ram lines have no Citadel equivalent).
local function logo(frame)
    local f1 = {
        { 0x7A, 0x8B, 0xFA, "O" }, { 0x73, 0x85, 0xEC, "ɴ" },
        { 0x6B, 0x7F, 0xDE, "ɪ" }, { 0x64, 0x79, 0xD0, "x " },
        { 0x5C, 0x73, 0xC2, "M" }, { 0x55, 0x6D, 0xB4, "ɪ" },
        { 0x4D, 0x67, 0xA6, "ɴ" }, { 0x46, 0x61, 0x98, "ɪ" },
        { 0x3E, 0x5B, 0x8A, "ɢ" }, { 0x37, 0x55, 0x7C, "ᴀ" },
        { 0x2F, 0x4F, 0x6E, "ᴍ" }, { 0x28, 0x49, 0x60, "ᴇ" },
        { 0x20, 0x43, 0x52, "s" },
    }
    local f2 = {
        { 0x73, 0x85, 0xEC, "O" }, { 0x7A, 0x8B, 0xFA, "ɴ" },
        { 0x73, 0x85, 0xEC, "ɪ" }, { 0x6B, 0x7F, 0xDE, "x " },
        { 0x64, 0x79, 0xD0, "M" }, { 0x5C, 0x73, 0xC2, "ɪ" },
        { 0x55, 0x6D, 0xB4, "ɴ" }, { 0x4D, 0x67, 0xA6, "ɪ" },
        { 0x46, 0x61, 0x98, "ɢ" }, { 0x3E, 0x5B, 0x8A, "ᴀ" },
        { 0x37, 0x55, 0x7C, "ᴍ" }, { 0x2F, 0x4F, 0x6E, "ᴇ" },
        { 0x28, 0x49, 0x60, "s" },
    }
    local runs = {}
    for _, t in (frame == 1 and f1 or f2) do
        table.insert(runs, {
            t[4],
            color = color(t[1] / 255, t[2] / 255, t[3] / 255),
            bold = true, italic = true,
        })
    end
    return runs
end

local function line()
    local runs = {}
    for i = 1, 36 do
        local f = (i - 1) / 35
        table.insert(runs, {
            "_",
            color = color((0xFF + (0xFF - 0xFF) * f) / 255,
                          (0xFF + (0xFF - 0xFF) * f) / 255,
                          (0x0F + (0x92 - 0x0F) * f) / 255),
        })
    end
    return runs
end

local function set_tab(frame)
    ui.tab{
        header = { line(), logo(frame), "" },
        footer = {
            { { "ᴏɴʟɪɴᴇ: ", color = "gray" }, { tostring(players.count()), color = "yellow" } },
            "",
            line(),
        },
    }
end

set_tab(1)
task.spawn(function()
    local frame = 1
    while true do
        task.wait(3)
        frame = frame == 1 and 2 or 1
        set_tab(frame)
    end
end)

-- ---- players ----------------------------------------------------------------

-- Essentials' motd.txt, the four gold lines a joiner saw:
--   &6Welcome, {PLAYER}&6! / Type &c/help&6... / Type &c/list&6... /
--   Players online:&c {ONLINE} &6- World time:&c {WORLDTIME12}
local function world_time12()
    local t = world.time()
    if type(t) ~= "number" then return "6:00 AM" end
    local h = math.floor(t / 1000 + 6) % 24
    local m = math.floor((t % 1000) / 1000 * 60)
    local h12 = h % 12
    if h12 == 0 then h12 = 12 end
    return string.format("%d:%02d %s", h12, m, h < 12 and "AM" or "PM")
end

local function essentials_motd(p)
    p:message({
        { "Welcome, ", color = "gold" },
        { p.name, color = "gold" },
        { "!", color = "gold" },
    })
    p:message({
        { "Type ", color = "gold" },
        { "/help", color = "red" },
        { " for a list of commands.", color = "gold" },
    })
    p:message({
        { "Type ", color = "gold" },
        { "/list", color = "red" },
        { " to see who else is online.", color = "gold" },
    })
    p:message({
        { "Players online: ", color = "gold" },
        { tostring(players.count()), color = "red" },
        { " - World time: ", color = "gold" },
        { world_time12(), color = "red" },
    })
end

-- One boot question, asked the first time the world around the spawn is
-- actually loaded (a read before that is nil — Citadel never generates a
-- chunk to answer one): the live Skript teleports players INSIDE the
-- maps' invisible light pillars and the falls are original behaviour, so
-- say what the engine really holds at the exact point and whether its
-- light block is solid. A registry that remaps light to something solid
-- would then show up here, in the console, instead of in play.
local spawn_probed = false
local function spawn_probe()
    if spawn_probed then return end
    local at = arena.spawn("lobby")
    local x, y, z = math.floor(at.x), math.floor(at.y), math.floor(at.z)
    local feet = world.get_block(vec3(x, y, z))
    if not feet then return end   -- chunk not loaded yet; ask again next join
    spawn_probed = true
    local light = game.block("light")
    citadel.log("[onixmg] spawn column @ " .. tostring(at)
        .. ": feet=" .. tostring(feet)
        .. " under=" .. tostring(world.get_block(vec3(x, y - 1, z)))
        .. "; light.material.solid=" .. tostring(light and light.material and light.material.solid))
end

players.on_join(function(p)
    core.on_join(p)          -- the Skript's spawn(); no welcome of its own
    essentials_motd(p)        -- Essentials sent these next
    set_tab(1)
    spawn_probe()
end)

players.on_leave(function(p)
    if core.S.phase == "Ingame" then
        -- the active game hears it first (Hot Potato passes the potato),
        -- then the Skript's intended mg_eliminate: announced, no teleport
        local g = core.games[core.S.active]
        if g and g.on_leave then g.on_leave(p) end
        core.eliminate(p, true)
    end
    core.refresh()
    set_tab(1)
end)

players.on_respawn(function(p)
    -- 1_Spawn.sk, verbatim: "on respawn: wait 1 tick; spawn(player)" — the
    -- lobby point, always, mid-game or not. (Respawning into an arena's
    -- exact point would re-drop a player through its light pillar every
    -- death; the live server never did that, and for Hot Potato it would
    -- loop: the 30-block spawn fall is lethal.)
    core.lobby(p)
end)

-- ---- input ---------------------------------------------------------------

players.on_click(function(p, hit)
    if core.S.phase == "Ingame" then
        local g = core.games[core.S.active]
        if g and g.on_click and core.in_roster(p) then
            g.on_click(p, hit)
        end
        return
    end

    if hit.slot == 1 then
        menus.vote(p)
    elseif hit.slot == 2 then
        menus.profile(p, p)
    elseif hit.slot == 5 then
        core.discord_broadcast(p)
        p:sound("entity.experience_orb.pickup", { volume = 0.5, pitch = 1 })
    end
end)

-- Damage is the game's question to answer: the holder's hits in Hot
-- Potato are refused, and every other game — the lobby included — takes
-- its hits as the old server did.
players.on_damage(function(p, hit)
    if core.S.phase == "Ingame" then
        local g = core.games[core.S.active]
        if g and g.on_damage then
            return g.on_damage(p, hit)
        end
    end
end)

-- ---- commands ------------------------------------------------------------

commands.add("vote <game:word>", function(p, args)
    core.cast_vote(p, args.game)
end, {
    help = "Vote for the next minigame",
    suggest = {
        game = function()
            return core.S.phase == "Lobby" and core.order or {}
        end,
    },
})

-- The Skript gave /startgame and /stopgame a 2-second cooldown each.
local function on_cooldown(p, key, seconds)
    local now = time.now()
    local last = p.data[key] or -100
    if now - last < seconds then return true end
    p.data[key] = now
    return false
end

commands.add("startgame", function(p)
    if not menus.is_admin(p) then return "You do not have permission." end
    if on_cooldown(p, "cmd_startgame", 2) then return end

    if not core.S.running then
        -- an addition: the Skript could only be restarted by reloading
        core.start()
        core.tell(p, "System started.", "green")
        return
    end
    if not core.skip_vote(p) then
        -- "&7Server is in &e%state%&7 state." with the anvil
        core.deny_runs(p, {
            { "Server is in ", color = "gray" },
            { core.S.phase, color = "yellow" },
            { " state.", color = "gray" },
        })
    end
end, { help = "Skip the vote wait" })

commands.add("stopgame", function(p)
    if not menus.is_admin(p) then return "You do not have permission." end
    if on_cooldown(p, "cmd_stopgame", 2) then return end
    if not core.stop() then
        core.deny(p, "System is already disabled!")
    end
end, { help = "Shut the cycle down" })

-- /settimer <number>: the old command wrote the variable and answered
-- with nothing but its debug line.
commands.add("settimer <seconds:integer 1..>", function(p, args)
    if not menus.is_admin(p) then return "You do not have permission." end
    core.set_timer(args.seconds, p)
end, { help = "Set the current timer" })

-- /changemapstate [<text>]: direct paste with no reply, the GUI otherwise,
-- exactly as the Skript had it (the mid-game guard is this port's own).
commands.add("changemapstate [state:word]", function(p, args)
    if not menus.is_admin(p) then return "You do not have permission." end
    if core.S.phase == "Ingame" then
        return "The map cannot change during a game."
    end
    if args.state then
        if not arena.show(args.state) then
            return "No map state named " .. args.state .. "."
        end
        arena.send(p, "lobby")   -- the Skript's spawn() after the click
        core.refresh()
    else
        menus.map_states(p)
    end
end, {
    help = "Open the map state picker, or paste a state directly",
    suggest = { state = function() return arena.maps() end },
})

commands.add("eliminate <target:player>", function(p, args)
    if not menus.is_admin(p) then return "You do not have permission." end
    if not core.eliminate(args.target) then
        return "That player is not in a round."
    end
end, { help = "Remove a player from the round" })

-- /spawn [player]: onix.spawn, 3-second cooldown, admins may send someone
-- else — and the Skript ran spawn() for the sender at the end either way.
commands.add("spawn [target:player]", function(p, args)
    local now = time.now()
    local last = p.data.spawn_last or -100
    if now - last < 3 then
        core.tell(p, string.format(
            "Please wait %d seconds before using /spawn again.",
            math.ceil(3 - (now - last))), "red")
        return
    end
    p.data.spawn_last = now

    if args.target and args.target ~= p then
        if not menus.is_admin(p) then
            core.tell(p, "Only administrators can teleport other players.", "red")
            return
        end
        core.lobby(args.target)
        p:message({
            { "You have teleported ", color = "gray" },
            { args.target.name, color = "white" },
            { " to spawn.", color = "gray" },
        })
    end

    -- and spawn(player), whatever else happened above
    if core.S.phase == "Ingame" and core.in_roster(p) then
        core.eliminate(p)   -- the Spleef Skript's "on command /spawn"
    else
        core.lobby(p)
    end
end, { aliases = { "hub" }, help = "Return to spawn" })

-- /center [yaw] [pitch]: onix.admin, block-centre snap, the yellow
-- confirmation and the soft teleport chime.
commands.add("center [yaw:number] [pitch:number]", function(p, args)
    if not menus.is_admin(p) then
        return "You do not have permission to center yourself."
    end
    local at = p.at
    local rot = p.rotation
    p:teleport(
        vec3(math.floor(at.x) + 0.5, math.floor(at.y), math.floor(at.z) + 0.5),
        { yaw = args.yaw or rot.yaw, pitch = args.pitch or rot.pitch }
    )
    core.tell(p, "You have been centered!", "yellow")
    p:sound("entity.enderman.teleport", { volume = 0.5, pitch = 2 })
end, {
    help = "Snap to the centre of your block",
    suggest = {
        yaw = { "0", "90", "180", "-90" },
        pitch = { "0", "90", "-90" },
    },
})

-- Utils/2_Discord.sk: /discord with its four aliases.
commands.add("discord", function(p)
    core.discord_broadcast(p)
    p:sound("entity.experience_orb.pickup", { volume = 0.5, pitch = 1 })
end, {
    aliases = { "dc", "dcserver", "discordserver", "onixdiscord" },
    help = "Join the official discord server",
})

-- /list, so the welcome's third line tells the truth (vanilla's wording).
commands.add("list", function(p)
    local names = {}
    for _, q in players.list() do table.insert(names, q.name) end
    core.tell(p, "There are " .. #names .. " players online: " .. table.concat(names, ", "))
end, { help = "See who else is online" })

commands.add("profile [target:player]", function(p, args)
    menus.profile(p, args.target or p)
end, { help = "Your stats, or another player's" })

commands.add("adminpanel", function(p)
    menus.admin(p)
end, { aliases = { "ap" }, help = "Open the admin panel" })

-- ---- announcements ---------------------------------------------------------

-- "every 2 minutes" from Utils/2_Discord.sk: the link, and the soft note.
task.spawn(function()
    while true do
        task.wait(120)
        if players.count() > 0 then
            core.discord_broadcast()
            sound.play("block.note_block.bit", { volume = 0.3, pitch = 1.5 })
        end
    end
end)

-- ---- safety net ------------------------------------------------------------

-- The arena floats well above the void; nobody should ever be below it.
task.spawn(function()
    while true do
        task.wait(1)
        for _, p in players.list() do
            local at = p.at
            if at and at.y < 50 then
                if core.S.phase == "Ingame" and core.in_roster(p) then
                    core.eliminate(p)
                else
                    core.lobby(p)
                end
            end
        end
    end
end)

task.spawn(core.run)

citadel.log("[onixmg] ready")

