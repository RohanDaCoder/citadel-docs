--!nonstrict
-- games/hotpotato.luau — pass the potato before it goes off.
--
-- Ported from plugins/Skript/scripts/Games/3_HotPotato.sk, as the live
-- server runs it:
--   * a random starter gets the potato: "&e%name% &7has the potato!"
--   * the holder's hits are cancelled ("cancel event if holder is
--     attacker"), so the holder cannot pass it; anyone ELSE who hits a
--     player passes the potato to the VICTIM — "&e%attacker% &apassed the
--     potato to &e%victim%", with the flap for everyone
--   * the round runs inside mg_start_game's 120 s timer
--   * the holder leaving: "&cThe potato holder left! Giving potato to a
--     random player"
--
-- Two deviations, both because the Skript was broken:
--   * its "while timer <= 0" main loop could never run — the potato was
--     taken back the second it was given and the BOOM never fired. Here
--     the fuse counts down from 30 s, plays the explode sound, broadcasts
--     the intended "&c&lBOOM! &e%name% &7exploded!" and eliminates the
--     holder, then the potato finds a new random holder
--   * the quit handler only said "Giving potato to a random player";
--     here it actually gives it

local core = require("core")

local hotpotato = {
    name = "Hot Potato",
    key = "hotpotato",
    arena = "hotpotato",
    blurb = "Tag your opponents!",
    icon = "baked_potato",
    title_color = "gold",   -- "&6&lHot Potato" in mg_start_game
    votable = false,        -- commented out of {minigames::list::*} on live
    duration = 120,         -- mg_start_game's round timer
    void_y = nil,           -- 3_HotPotato.sk never had a y-check: the arena
                            -- floor sits below the other games' kill line
}

local POTATO_SECONDS = 30   -- mg_hot_potato_cycle's own timer

local holder = nil
local countdown = 0

-- Citadel's hotbar is whole-bar, so the holder gets the potato where the
-- compass was and everyone else keeps the lobby items.
local function hand_out()
    for _, p in core.S.roster do
        if p == holder then
            p:hotbar{
                [1] = {
                    item = "baked_potato",
                    name = "Hot Potato",
                    lore = { "Hit someone to pass it on" },
                    glint = true,
                },
                [2] = { item = "book", name = "Profile", lore = { "Your stats" } },
                [5] = { item = "paper", name = "Discord", lore = { core.DISCORD } },
            }
        else
            p:hotbar{
                [1] = { item = "compass", name = "Vote", lore = { "Choose the next game" } },
                [2] = { item = "book", name = "Profile", lore = { "Your stats" } },
                [5] = { item = "paper", name = "Discord", lore = { core.DISCORD } },
            }
        end
    end
end

local function assign()
    local roster = core.S.roster
    if #roster == 0 then
        holder = nil
        return
    end
    holder = roster[math.random(#roster)]
    countdown = POTATO_SECONDS
    core.bump(holder.uuid, "hotpotato_touches")
    core.broadcast_runs({
        { holder.name, color = "yellow" },
        { " has the potato!", color = "gray" },
    })
    hand_out()
end

function hotpotato.start()
    holder = nil
    countdown = 0
    assign()
end

function hotpotato.stop()
    holder = nil
end

function hotpotato.step(dt)
    if not holder or not core.in_roster(holder) then
        assign()
        return
    end

    countdown = countdown - dt
    if countdown > 0 then return end

    local victim = holder
    holder = nil
    sound.play("entity.generic.explode", { volume = 1, pitch = 1 })
    core.broadcast_runs({
        { "BOOM! ", color = "red", bold = true },
        { victim.name, color = "yellow" },
        { " exploded!", color = "gray" },
    })
    core.eliminate(victim)
    if core.S.phase == "Ingame" then assign() end
end

-- The old "on quit" case: the holder leaving announces and passes the
-- potato to a new random player.
function hotpotato.on_leave(p)
    if holder and p == holder then
        holder = nil
        countdown = 0
        core.broadcast("The potato holder left! Giving potato to a random player", "red")
    end
end

-- The live transfer, in its exact direction: a NON-holder hits a player
-- and the VICTIM receives the potato; the holder's own hits are refused
-- outright.
function hotpotato.on_damage(victim, hit)
    local attacker = hit.by
    if not attacker or attacker == victim then return end

    if attacker == holder then
        return false   -- "cancel event if holder is attacker"
    end

    if holder and core.in_roster(victim) and core.in_roster(attacker) then
        local from = attacker
        holder = victim
        countdown = POTATO_SECONDS
        task.defer(function()
            core.bump(victim.uuid, "hotpotato_touches")
            core.broadcast_runs({
                { from.name, color = "yellow" },
                { " passed the potato to ", color = "green" },
                { victim.name, color = "yellow" },
            })
            sound.play("entity.ender_dragon.flap", { volume = 1, pitch = 1 })
            hand_out()
        end)
    end
end

return hotpotato
