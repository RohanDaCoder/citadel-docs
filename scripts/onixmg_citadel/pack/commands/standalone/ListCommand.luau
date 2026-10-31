--!nonstrict
-- commands/standalone/ListCommand.luau
-- /list — vanilla's wording, so the welcome's third line tells the truth.

local Messages = require("core/Messages")

return {
    name = "list",
    help = "See who else is online",
    handler = function(p)
        local names = {}
        for _, q in players.list() do table.insert(names, q.name) end
        Messages.tell(p, "There are " .. #names .. " players online: " .. table.concat(names, ", "))
    end,
}
