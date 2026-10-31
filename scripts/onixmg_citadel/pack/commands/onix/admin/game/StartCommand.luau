--!nonstrict
-- commands/onix/admin/game/StartCommand.luau
-- /onix admin game start — 2 s cooldown. A stopped system starts; a
-- running vote is cut to five seconds and the skipper is named; any other
-- state is denied with the state line.

local state = require("core/GameState")
local Messages = require("core/Messages")
local CycleControls = require("core/CycleControls")

return {
    usage = "admin game start",
    help = "Skip the vote wait",
    admin = true,
    cooldown = 2,
    handler = function(p)
        if not state.running then
            CycleControls:start()
            Messages.tell(p, "System started.", "green")
            return
        end
        if not CycleControls:skipVote(p) then
            Messages.deny_runs(p, {
                { "Server is in ", color = "gray" },
                { state.phase, color = "yellow" },
                { " state.", color = "gray" },
            })
        end
    end,
}
