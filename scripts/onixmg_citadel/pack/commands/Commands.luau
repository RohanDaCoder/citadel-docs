--!nonstrict
-- commands/Commands.luau
-- One purpose: the pack's command catalog — the explicit list of command
-- modules, each registered through the shared Registrar. Adding a
-- command means adding its one file and one line here.

local Registrar = require("commands/Registrar")

local Commands = {}

function Commands.register()
    local specs = {
        require("commands/VoteCommand"),
        require("commands/StartGameCommand"),
        require("commands/StopGameCommand"),
        require("commands/SetTimerCommand"),
        require("commands/ChangeMapStateCommand"),
        require("commands/EliminateCommand"),
        require("commands/SpawnCommand"),
        require("commands/CenterCommand"),
        require("commands/DiscordCommand"),
        require("commands/ListCommand"),
        require("commands/ProfileCommand"),
        require("commands/AdminPanelCommand"),
    }
    for _, spec in specs do
        Registrar.add(spec)
    end
end

return Commands
