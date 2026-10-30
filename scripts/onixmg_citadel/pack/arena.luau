--!nonstrict
-- arena.luau — the six map states, where each pastes, and where players stand.
--
-- The maps are the live Paper server's FAWE schematics, downloaded from
-- plugins/FastAsyncWorldEdit/schematics/ on 2026-10-30 and used byte for
-- byte. A Sponge v2 schematic carries `Offset`: the original world
-- position of the block at its own (0, 0, 0), and Fawesk's paste
-- reproduced the maps at exactly those coordinates, so pasting at
-- Offset + SHIFT here rebuilds the live arenas block for block, lifted
-- into Citadel's 0..255 world.
--
-- The live spawn points sit inside sealed light boxes a few blocks above
-- each arena floor (Hot Potato's is 31 blocks up). `floor` is the exact
-- tile each spawn lands on, read out of the schematic's own blocks: a
-- player arrives standing on the floor instead of falling to it, and no
-- ground scan is done at runtime — Citadel keeps unloaded chunks
-- invisible to world.get_block, and at load time nothing is loaded.
--
-- The void threshold is the Skript's y < -48, lifted with the same SHIFT
-- (Spleef, TNT Run and Sumo eliminated at it; Hot Potato never had one,
-- its floor is below the line, so it keeps none here either).

local arena = {}

-- old world (x, y, z) -> Citadel (x + 5, y + 117, z - 35)
arena.SHIFT = vec3(5, 117, -35)
arena.VOID_Y = -48 + arena.SHIFT.y   -- 69: the Skript's kill line, lifted

local MAPS = {
    lobby = {
        file = "builds/OnixMG_state_lobby.schem",
        offset = vec3(-51, -52, -1),
        spawn = vec3(-46.5, -18.0, 38.5),
        yaw = -90,
        floor = 97,   -- on the basalt lobby floor (local 31)
    },
    spleef = {
        file = "builds/OnixMG_state_spleef.schem",
        offset = vec3(-51, -52, -1),
        spawn = vec3(1.5, -20.0, 35.5),
        yaw = 90,
        floor = 86,   -- on the snow platform (local 20)
    },
    tntrun = {
        file = "builds/OnixMG_state_tntrun.schem",
        offset = vec3(-51, -52, -1),
        spawn = vec3(-23.5, -20.0, 38.5),
        yaw = 90,
        floor = 85,   -- on the green concrete step (local 19)
    },
    hotpotato = {
        file = "builds/OnixMG_state_hotpotato.schem",
        offset = vec3(-51, -52, -1),
        spawn = vec3(1.5, -20.0, 35.5),
        yaw = 90,
        floor = 67,   -- on the grass island (local 1), below the kill line
    },
    sumo = {
        file = "builds/OnixMG_state_sumo.schem",
        offset = vec3(-51, -52, -1),
        spawn = vec3(4.5, -15.0, 33.5),
        yaw = 90,
        floor = 94,   -- on the gold sumo ring (local 28)
    },
    empty = {
        -- the sixth state the old server kept in its schematics folder,
        -- reachable through /changemapstate empty but offered by no GUI
        file = "builds/OnixMG_state_empty.schem",
        offset = vec3(-51, -52, -1),
        spawn = vec3(-46.5, -18.0, 38.5),
        yaw = -90,
        floor = 97,
    },
}

local schem, origin = {}, {}

for key, def in MAPS do
    schem[key] = world.schematic(def.file)
    origin[key] = def.offset + arena.SHIFT
end

arena.current = nil

function arena.has(name)
    return schem[name] ~= nil
end

function arena.maps()
    local out = {}
    for key in MAPS do
        if schem[key] then table.insert(out, key) end
    end
    table.sort(out)
    return out
end

--- Put one map state in the world, replacing whatever was there.
--- world.paste writes live, stored and sent, whether or not any player
--- is near; the chunks need not be loaded for the blocks to be there.
--- `part` names each paste so render-build and check-build can frame it.
function arena.show(name)
    if not schem[name] then return false end
    world.paste(schem[name], origin[name], { air = true, part = name })
    arena.current = name
    return true
end

--- Fill chunks as they come into memory with the map that is showing.
function arena.install()
    world.on_generate(function(chunk)
        local name = arena.current
        if name and schem[name] then
            chunk:paste(schem[name], origin[name], { air = true, part = name })
        end
    end)
end

--- Where a player's feet go for a map: the old spawn's column, on the
--- floor tile the schematic puts there.
function arena.spawn(name)
    local def = MAPS[name]
    if not def then return vec3(0, 100, 0) end
    local at = def.spawn + arena.SHIFT
    return vec3(at.x, def.floor, at.z)
end

function arena.yaw(name)
    return MAPS[name] and MAPS[name].yaw or 0
end

function arena.send(player, name)
    player:teleport(arena.spawn(name), { yaw = arena.yaw(name), pitch = 0 })
end

return arena
