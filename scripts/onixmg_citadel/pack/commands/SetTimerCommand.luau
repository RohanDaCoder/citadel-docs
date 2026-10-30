--!nonstrict
-- commands/SetTimerCommand.luau
-- /settimer <seconds> — admin. Steers the live countdown (the old
-- command wrote the variable and only its debug line ever said so).

local CycleControls = require("core/CycleControls")

return {
    name = "settimer <seconds:integer 1..>",
    help = "Set the current timer",
    admin = true,
    handler = function(p, args)
        CycleControls:setTimer(args.seconds, p)
    end,
}
