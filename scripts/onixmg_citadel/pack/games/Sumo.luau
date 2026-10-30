--!nonstrict
-- games/Sumo.luau
-- Shove everyone else off the ring. No hooks of its own: the ring is
-- ordinary punching (vanilla melee damage and knockback), and the void
-- check (y < 69) is the cycle loop's. votable = false (commented out of
-- the live server's votable list).

local Game = require("games/Game")

local Sumo = setmetatable({}, { __index = Game })
Sumo.__index = Sumo

function Sumo.new()
    local self = Game.new({
        name = "Sumo",
        key = "sumo",
        arena = "sumo",
        blurb = "Punch off opponents out of the arena!",
        icon = "player_head",
        title_color = "dark_red",
        votable = false,
        duration = 120,
        void_y = 69,
    })
    return setmetatable(self, Sumo)
end

return Sumo.new()
