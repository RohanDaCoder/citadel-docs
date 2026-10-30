--!nonstrict
-- games/HotPotato.luau
-- Pass the potato before it goes off. A random starter gets the potato
-- ("X has the potato!"), the holder's hits are refused, and anyone else
-- who hits a player passes the potato to the victim ("X passed the
-- potato to Y"). The fuse counts down from 30s; at zero the holder
-- explodes (BOOM!), is eliminated, and a new random holder is chosen.
-- If the holder leaves, the potato passes to a new random player.
-- votable = false (commented out on the live server); void_y = nil.

local Game = require("games/Game")
local Eliminator = require("core/Eliminator")
local Hotbar = require("ui/Hotbar")

local HotPotato = setmetatable({}, { __index = Game })
HotPotato.__index = HotPotato

function HotPotato.new()
    local self = Game.new({
        name = "Hot Potato",
        key = "hotpotato",
        arena = "hotpotato",
        blurb = "Tag your opponents!",
        icon = "baked_potato",
        title_color = "gold",
        votable = false,
        duration = 120,
        void_y = nil,
    })
    self._holder = nil
    self._countdown = 0
    return setmetatable(self, HotPotato)
end

local POTATO_SECONDS = 30   -- the fuse the live Skript intended

-- Citadel's hotbar is whole-bar, so the holder gets the potato where the
-- compass was and everyone else keeps the lobby items.
function HotPotato:_handOut()
    for _, p in self:roster() do
        if p == self._holder then
            p:hotbar{
                [1] = {
                    item = "baked_potato",
                    name = "Hot Potato",
                    lore = { "Hit someone to pass it on" },
                    glint = true,
                },
                [2] = { item = "book", name = "Profile", lore = { "Your stats" } },
                [5] = { item = "paper", name = "Discord", lore = { self:discord() } },
            }
        else
            Hotbar.lobby(p)
        end
    end
end

function HotPotato:_assign()
    local roster = self:roster()
    if #roster == 0 then
        self._holder = nil
        return
    end
    self._holder = roster[math.random(#roster)]
    self._countdown = POTATO_SECONDS
    self:bumpStat(self._holder.uuid, "hotpotato_touches")
    self:broadcastRuns({
        { self._holder.name, color = "yellow" },
        { " has the potato!", color = "gray" },
    })
    self:_handOut()
end

function HotPotato:onStart()
    self._holder = nil
    self._countdown = 0
    self:_assign()
end

function HotPotato:onStop()
    self._holder = nil
end

function HotPotato:onStep(dt)
    if not self._holder or not self:inRoster(self._holder) then
        self:_assign()
        return
    end

    self._countdown = self._countdown - dt
    if self._countdown > 0 then return end

    local victim = self._holder
    self._holder = nil
    sound.play("entity.generic.explode", { volume = 1, pitch = 1 })
    self:broadcastRuns({
        { "BOOM! ", color = "red", bold = true },
        { victim.name, color = "yellow" },
        { " exploded!", color = "gray" },
    })
    Eliminator:eliminate(victim)
    if self:phase() == "Ingame" then self:_assign() end
end

-- The holder leaving announces and passes the potato to a new random player.
function HotPotato:onLeave(p)
    if self._holder and p == self._holder then
        self._holder = nil
        self._countdown = 0
        self:broadcast("The potato holder left! Giving potato to a random player", "red")
    end
end

-- The live transfer, in its exact direction: a NON-holder hits a player
-- and the VICTIM receives the potato; the holder's own hits are refused.
function HotPotato:onDamage(victim, hit)
    local attacker = hit.by
    if not attacker or attacker == victim then return end

    if attacker == self._holder then
        return false   -- "cancel event if holder is attacker"
    end

    if self._holder and self:inRoster(victim) and self:inRoster(attacker) then
        local from = attacker
        self._holder = victim
        self._countdown = POTATO_SECONDS
        task.defer(function()
            self:bumpStat(victim.uuid, "hotpotato_touches")
            self:broadcastRuns({
                { from.name, color = "yellow" },
                { " passed the potato to ", color = "green" },
                { victim.name, color = "yellow" },
            })
            sound.play("entity.ender_dragon.flap", { volume = 1, pitch = 1 })
            self:_handOut()
        end)
    end
end

return HotPotato.new()
