--!nonstrict
-- commands/onix/players/EliminateCommand.luau
-- /onix players eliminate <player> — remove a player from the running
-- round.

local Eliminator = require("core/Eliminator")

return {
    usage = "players eliminate <target:player>",
    help = "Remove a player from the round",
    admin = true,
    handler = function(_, args)
        if not Eliminator:eliminate(args.target) then
            return "That player is not in a round."
        end
    end,
}
