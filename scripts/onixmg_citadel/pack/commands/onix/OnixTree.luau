--!nonstrict
-- commands/onix/OnixTree.luau
-- One purpose: the /onix command tree — the catalog of every subcommand
-- (one file per leaf, the folder path mirroring the command path) plus the
-- bare /onix line that lists the tree. Each leaf is registered as its own
-- shape of the single "onix" command:
--   /onix <group> [sub-group] <command> [args]
--     /onix admin game start|stop   /onix admin timer <seconds>
--     /onix admin panel             /onix admin center [yaw] [pitch]
--     /onix players eliminate <player>
--     /onix map changemapstate [state]
-- Player-facing commands (/vote, /spawn, /discord, /list, /profile) are
-- deliberately NOT part of this tree; they stay standalone in
-- commands/standalone/.

local Registrar = require("commands/Registrar")
local Messages = require("core/Messages")

local SPECS = {
    require("commands/onix/admin/game/StartCommand"),
    require("commands/onix/admin/game/StopCommand"),
    require("commands/onix/admin/TimerCommand"),
    require("commands/onix/admin/PanelCommand"),
    require("commands/onix/admin/CenterCommand"),
    require("commands/onix/players/EliminateCommand"),
    require("commands/onix/map/ChangeMapStateCommand"),
}

-- "admin timer <seconds:integer 1..>" -> "admin timer <seconds>": the
-- listing shows what to type, not the grammar.
local function pretty(usage)
    return (usage:gsub(":[^%>%]]+", ""))
end

local OnixTree = {}

function OnixTree.register()
    for _, spec in SPECS do
        Registrar.add_onix(spec)
    end

    -- The bare /onix line, registered last so a full line always fits a
    -- real shape first. Admin-gated like the rest of the tree; lists each
    -- subcommand with its help line.
    Registrar.add_onix({
        usage = "",
        help = "List the onix subcommands",
        admin = true,
        handler = function(p)
            for _, spec in SPECS do
                p:message(Messages.cat(Messages.prefix_runs(), {
                    { "/onix " .. pretty(spec.usage), color = "white" },
                    { " - " .. spec.help, color = "gray" },
                }))
            end
        end,
    })
end

return OnixTree
