--!nonstrict
-- core/Arena.luau
-- The six map states: where each pastes, and where players stand. The
-- maps are the live Paper server's FAWE schematics, pasted at Offset +
-- SHIFT so the arenas rebuild block for block in Citadel's 0..255 world.
-- Each spawn point is the live Skript's own coordinate, lifted by the
-- same SHIFT; every one sits inside its map's invisible light pillar, so
-- the fall to the floor (and the game's fall damage) is original
-- behaviour, kept on purpose.
--
-- One instance exists for the whole pack; subsystems require this module
-- and call its methods on the returned singleton.

local Arena = {}
Arena.__index = Arena

-- old world (x, y, z) -> Citadel (x + 5, y + 117, z - 35)
Arena.SHIFT = vec3(5, 117, -35)
Arena.VOID_Y = -48 + Arena.SHIFT.y   -- 69: the Skript's kill line, lifted

local MAPS = {
    lobby = {
        file = "builds/OnixMG_state_lobby.schem",
        offset = vec3(-51, -52, -1),
        spawn = vec3(-46.5, -18.0, 38.5),   -- 1_Spawn.sk: (-46.5, -18, 38.5, -90, 0)
        yaw = -90,
    },
    spleef = {
        file = "builds/OnixMG_state_spleef.schem",
        offset = vec3(-51, -52, -1),
        spawn = vec3(1.5, -20.0, 35.5),     -- 1_CoreSystem.sk: (1.5, -20, 35.5, 90, 0)
        yaw = 90,
    },
    tntrun = {
        file = "builds/OnixMG_state_tntrun.schem",
        offset = vec3(-51, -52, -1),
        spawn = vec3(-23.5, -20.0, 38.5),   -- 1_CoreSystem.sk: (-23.5, -20, 38.5, 90, 0)
        yaw = 90,
    },
    hotpotato = {
        file = "builds/OnixMG_state_hotpotato.schem",
        offset = vec3(-51, -52, -1),
        spawn = vec3(1.5, -20.0, 35.5),     -- 1_CoreSystem.sk: (1.5, -20, 35.5, 90, 0)
        yaw = 90,
    },
    sumo = {
        file = "builds/OnixMG_state_sumo.schem",
        offset = vec3(-51, -52, -1),
        spawn = vec3(4.5, -15.0, 33.5),     -- 1_CoreSystem.sk: (4.5, -15, 33.5, 90, 0)
        yaw = 90,
    },
    empty = {
        file = "builds/OnixMG_state_empty.schem",
        offset = vec3(-51, -52, -1),
        spawn = vec3(-46.5, -18.0, 38.5),   -- no arena; the lobby's point serves
        yaw = -90,
    },
}

function Arena:has(name)
    return self._schem[name] ~= nil
end

function Arena:maps()
    local out = {}
    for key in MAPS do
        if self._schem[key] then table.insert(out, key) end
    end
    table.sort(out)
    return out
end

-- Put one map state in the world, replacing whatever was there. world.paste
-- writes live, stored and sent, whether or not any player is near; the
-- chunks need not be loaded for the blocks to be there. `part` names each
-- paste so render-build and check-build can frame it.
function Arena:show(name)
    if not self._schem[name] then return false end
    world.paste(self._schem[name], self._origin[name], { air = true, part = name })
    self.current = name
    return true
end

-- Fill chunks as they come into memory with the map that is showing.
function Arena:install()
    world.on_generate(function(chunk)
        local name = self.current
        if name and self._schem[name] then
            chunk:paste(self._schem[name], self._origin[name], { air = true, part = name })
        end
    end)
end

-- Where a player's feet go for a map: the live Skript's own coordinates,
-- exactly, lifted by the same SHIFT as the pastes.
function Arena:spawn(name)
    local def = MAPS[name]
    if not def then return vec3(0, 100, 0) end
    return def.spawn + self.SHIFT
end

function Arena:yaw(name)
    return MAPS[name] and MAPS[name].yaw or 0
end

function Arena:send(player, name)
    player:teleport(self:spawn(name), { yaw = self:yaw(name), pitch = 0 })
end

local arena = setmetatable({ current = nil, _schem = {}, _origin = {} }, Arena)
for key, def in MAPS do
    arena._schem[key] = world.schematic(def.file)
    arena._origin[key] = def.offset + Arena.SHIFT
end
return arena
