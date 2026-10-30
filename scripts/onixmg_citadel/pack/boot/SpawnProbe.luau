--!nonstrict
-- boot/SpawnProbe.luau
-- One purpose: the one-shot boot question — the first time the world
-- around the spawn is actually loaded (a read before that is nil:
-- Citadel never generates a chunk to answer one), log what the engine
-- really holds at the exact spawn point and whether its light block is
-- solid. A registry that remapped light to something solid would show up
-- here, in the console, instead of in play.

local Arena = require("core/Arena")

local SpawnProbe = {}

local probed = false

function SpawnProbe.check()
    if probed then return end
    local at = Arena:spawn("lobby")
    local x, y, z = math.floor(at.x), math.floor(at.y), math.floor(at.z)
    local feet = world.get_block(vec3(x, y, z))
    if not feet then return end   -- chunk not loaded yet; ask again next join
    probed = true
    local light = game.block("light")
    citadel.log("[onixmg] spawn column @ " .. tostring(at)
        .. ": feet=" .. tostring(feet)
        .. " under=" .. tostring(world.get_block(vec3(x, y - 1, z)))
        .. "; light.material.solid=" .. tostring(light and light.material and light.material.solid))
end

return SpawnProbe
