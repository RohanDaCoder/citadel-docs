--!nonstrict
-- boot/BootLog.luau
-- One purpose: the boot console lines — which maps loaded and where the
-- lobby spawn point is.

local Arena = require("core/Arena")

local BootLog = {}

function BootLog.log()
    citadel.log("[onixmg] maps: " .. table.concat(Arena:maps(), ", "))
    citadel.log("[onixmg] lobby spawn: " .. tostring(Arena:spawn("lobby")))
end

return BootLog
