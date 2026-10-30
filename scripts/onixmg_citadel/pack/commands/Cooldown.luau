--!nonstrict
-- commands/Cooldown.luau
-- Per-player command cooldowns, stored on the player's data table. Used
-- by /spawn (3s) and /startgame + /stopgame (2s each), as the live Skript
-- had them.

local Cooldown = {}

-- Returns true if the player is still on cooldown (and does NOT update
-- the timestamp); false otherwise (and records now).
function Cooldown.check(p, key, seconds)
    local now = time.now()
    local last = p.data[key] or -100
    if now - last < seconds then return true end
    p.data[key] = now
    return false
end

return Cooldown
