--!nonstrict
-- main.luau — the pack entry and composition root.
--
-- Requires the modules, registers the four games, installs the arena,
-- wires the player events (chat, join, leave, respawn, click, damage),
-- registers the slash commands, starts the background tasks (the tab logo
-- cycle, the two-minute Discord broadcast, the void safety net) and
-- launches the round cycle. Everything player-facing is delegated to the
-- core/ui/games modules; this file only wires them together.

local Arena = require("core/Arena")
local GameState = require("core/GameState")
local GameRegistry = require("core/GameRegistry")
local CycleDriver = require("core/CycleDriver")
local Messages = require("core/Messages")
local Menus = require("ui/Menus")
local Sidebar = require("ui/Sidebar")
local Tab = require("ui/Tab")
local Chat = require("ui/Chat")
local Motd = require("ui/Motd")
local Commands = require("commands/Commands")

-- Register the four games. Spleef and TNT Run are votable; Sumo and Hot
-- Potato register with votable = false (commented out on the live server).
GameRegistry:register(require("games/Spleef"))
GameRegistry:register(require("games/TNTRun"))
GameRegistry:register(require("games/Sumo"))
GameRegistry:register(require("games/HotPotato"))

Arena:install()
Arena:show("lobby")

citadel.log("[onixmg] maps: " .. table.concat(Arena:maps(), ", "))
citadel.log("[onixmg] lobby spawn: " .. tostring(Arena:spawn("lobby")))

-- ---- chat ----------------------------------------------------------------

players.on_chat(Chat.render)

-- ---- tab list ------------------------------------------------------------

Tab.set(1)
Tab.animate()

-- ---- join / leave / respawn ----------------------------------------------

-- One boot question, asked the first time the world around the spawn is
-- actually loaded (a read before that is nil — Citadel never generates a
-- chunk to answer one): say what the engine really holds at the exact
-- spawn point and whether its light block is solid. A registry that
-- remapped light to something solid would show up here, in the console.
local spawn_probed = false
local function spawn_probe()
    if spawn_probed then return end
    local at = Arena:spawn("lobby")
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
    CycleDriver:onJoin(p)     -- the Skript's spawn(); no welcome of its own
    Motd.welcome(p)           -- Essentials sent these next
    Tab.set(1)
    spawn_probe()
end)

players.on_leave(function(p)
    if GameState.phase == "Ingame" then
        -- the active game hears it first (Hot Potato passes the potato),
        -- then the elimination: announced, no teleport
        local g = GameRegistry:get(GameState.active)
        if g then g:onLeave(p) end
        CycleDriver:eliminate(p, true)
    end
    Sidebar.refresh()
    Tab.set(1)
end)

players.on_respawn(function(p)
    -- "on respawn: wait 1 tick; spawn(player)" — the lobby point, always,
    -- mid-game or not.
    CycleDriver:lobby(p)
end)

-- ---- input ---------------------------------------------------------------

players.on_click(function(p, hit)
    if GameState.phase == "Ingame" then
        local g = GameRegistry:get(GameState.active)
        if g and GameState:in_roster(p) then
            g:onClick(p, hit)
        end
        return
    end

    if hit.slot == 1 then
        Menus.vote(p)
    elseif hit.slot == 2 then
        Menus.profile(p, p)
    elseif hit.slot == 5 then
        Messages.discord_broadcast(p)
        p:sound("entity.experience_orb.pickup", { volume = 0.5, pitch = 1 })
    end
end)

-- Damage is the game's question to answer: the holder's hits in Hot
-- Potato are refused, and every other game takes its hits as the old
-- server did.
players.on_damage(function(p, hit)
    if GameState.phase == "Ingame" then
        local g = GameRegistry:get(GameState.active)
        if g then
            return g:onDamage(p, hit)
        end
    end
end)

-- ---- commands ------------------------------------------------------------

Commands.register()

-- ---- announcements -------------------------------------------------------

-- "every 2 minutes": the Discord link, and the soft note.
task.spawn(function()
    while true do
        task.wait(120)
        if players.count() > 0 then
            Messages.discord_broadcast()
            sound.play("block.note_block.bit", { volume = 0.3, pitch = 1.5 })
        end
    end
end)

-- ---- safety net ----------------------------------------------------------

-- The arena floats well above the void; nobody should ever be below it.
task.spawn(function()
    while true do
        task.wait(1)
        for _, p in players.list() do
            local at = p.at
            if at and at.y < 50 then
                if GameState.phase == "Ingame" and GameState:in_roster(p) then
                    CycleDriver:eliminate(p)
                else
                    CycleDriver:lobby(p)
                end
            end
        end
    end
end)

-- ---- cycle ---------------------------------------------------------------

task.spawn(function() CycleDriver:run() end)

citadel.log("[onixmg] ready")
