--!nonstrict
-- commands/StopGameCommand.luau
-- /stopgame — admin, 2 s cooldown. Shuts the cycle down; denying when it
-- is already disabled.

local Messages = require("core/Messages")
local CycleControls = require("core/CycleControls")

return {
    name = "stopgame",
    help = "Shut the cycle down",
    admin = true,
    cooldown = 2,
    handler = function(p)
        if not CycleControls:stop() then
            Messages.deny(p, "System is already disabled!")
        end
    end,
}
