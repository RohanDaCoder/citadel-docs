--!nonstrict
-- games/tntrun.luau — the floor crumbles behind every step.
--
-- Ported from plugins/Skript/scripts/Games/2_TNTRun.sk: "on walking on
-- green/yellow/red/gray concrete: wait 5 ticks, set the block to air, add
-- one to blocks broken". The old block-walk event is the round loop's
-- sampling here, and the count is the one mg_eliminate read back to the
-- player ("&7Blocks Broken: &e%N%") — silently, exactly as the old
-- server removed the block, so no sound plays.

local core = require("core")

local tntrun = {
    name = "TNT Run",
    key = "tntrun",
    arena = "tntrun",
    blurb = "Don't look down!",
    icon = "tnt",
    title_color = "red",   -- "&c&lTNT Run" in mg_start_game
    duration = 120,        -- mg_start_game's one timer, every game
    void_y = 69,           -- the Skript's y < -48, lifted by the SHIFT
}

local FLOOR = {
    green_concrete = true,
    yellow_concrete = true,
    red_concrete = true,
    gray_concrete = true,
}

local pending = {}   -- "x,y,z" -> { at = vec3, t = seconds, uuid = player }
local scan = 0

local function key(pos)
    return pos.x .. "," .. pos.y .. "," .. pos.z
end

function tntrun.start()
    pending = {}
    scan = 0
end

function tntrun.stop()
    pending = {}
end

function tntrun.step(dt)
    scan = scan + dt
    if scan >= 0.2 then
        scan = 0
        for _, p in players.list() do
            if core.in_roster(p) then
                local at = p.at
                local under = vec3(math.floor(at.x), math.floor(at.y - 1), math.floor(at.z))
                local block = world.get_block(under)
                if block and FLOOR[block] then
                    local k = key(under)
                    if not pending[k] then
                        pending[k] = { at = under, t = 0.25, uuid = p.uuid }
                    end
                end
            end
        end
    end

    for k, v in pending do
        v.t = v.t - dt
        if v.t <= 0 then
            pending[k] = nil
            world.set_block(v.at, "air")
            core.bump(v.uuid, "tntrun")
        end
    end
end

return tntrun
