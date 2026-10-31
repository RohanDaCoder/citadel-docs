--!nonstrict
-- commands/onix/admin/TimerCommand.luau
-- /onix admin timer <seconds> — steers the live countdown (the old
-- command wrote the variable and only its debug line ever said so).

local CycleControls = require("core/CycleControls")

return {
    usage = "admin timer <seconds:integer 1..>",
    help = "Set the current timer",
    admin = true,
    handler = function(p, args)
        CycleControls:setTimer(args.seconds, p)
    end,
}
