--!nonstrict
-- games/TNTRun.luau
-- The floor crumbles behind every step. Every 0.2s the block under each
-- rostered player is sampled; if it is green/yellow/red/gray concrete it
-- is scheduled to air 0.25s later and the player's "tntrun" stat bumps.
-- Silently, as the live server removed the block — no sound plays.

local Game = require("games/Game")

local TNTRun = setmetatable({}, { __index = Game })
TNTRun.__index = TNTRun

function TNTRun.new()
    local self = Game.new({
        name = "TNT Run",
        key = "tntrun",
        arena = "tntrun",
        blurb = "Don't look down!",
        icon = "tnt",
        title_color = "red",
        duration = 120,
        void_y = 69,
    })
    self._pending = {}
    self._scan = 0
    return setmetatable(self, TNTRun)
end

local FLOOR = {
    green_concrete = true,
    yellow_concrete = true,
    red_concrete = true,
    gray_concrete = true,
}

local function key(pos)
    return pos.x .. "," .. pos.y .. "," .. pos.z
end

function TNTRun:onStart()
    self._pending = {}
    self._scan = 0
end

function TNTRun:onStop()
    self._pending = {}
end

function TNTRun:onStep(dt)
    self._scan = self._scan + dt
    if self._scan >= 0.2 then
        self._scan = 0
        for _, p in players.list() do
            if self:inRoster(p) then
                local at = p.at
                local under = vec3(math.floor(at.x), math.floor(at.y - 1), math.floor(at.z))
                local block = world.get_block(under)
                if block and FLOOR[block] then
                    local k = key(under)
                    if not self._pending[k] then
                        self._pending[k] = { at = under, t = 0.25, uuid = p.uuid }
                    end
                end
            end
        end
    end

    for k, v in self._pending do
        v.t = v.t - dt
        if v.t <= 0 then
            self._pending[k] = nil
            world.set_block(v.at, "air")
            self:bumpStat(v.uuid, "tntrun")
        end
    end
end

return TNTRun.new()
