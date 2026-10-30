--!nonstrict
-- games/Spleef.luau
-- Dig the snow out from under everyone. A glinted shovel is placed in the
-- hotbar at start; left-clicking snow_block/snow/snow_layer clears it
-- with the snow-break sound. The void check (y < 69) is the cycle loop's.

local Game = require("games/Game")

local Spleef = setmetatable({}, { __index = Game })
Spleef.__index = Spleef

function Spleef.new()
    local self = Game.new({
        name = "Spleef",
        key = "spleef",
        arena = "spleef",
        blurb = "Dig your way to victory!",
        icon = "golden_shovel",
        title_color = "yellow",
        duration = 120,
        void_y = 69,
    })
    return setmetatable(self, Spleef)
end

local DIGGABLE = {
    snow_block = true,
    snow = true,
    snow_layer = true,
}

function Spleef:onStart()
    for _, p in players.list() do
        p:hotbar{
            [1] = {
                item = "golden_shovel",
                name = "Spleef Shovel",
                lore = { "Left click the snow" },
                glint = true,
            },
        }
    end
end

function Spleef:onClick(p, hit)
    if hit.button ~= "left" or not hit.block then return end

    local block = world.get_block(hit.block)
    if not block or not DIGGABLE[block] then return end

    world.set_block(hit.block, "air")
    p:sound("block.snow.break", { at = hit.block, volume = 0.8, pitch = 1 })
end

return Spleef.new()
