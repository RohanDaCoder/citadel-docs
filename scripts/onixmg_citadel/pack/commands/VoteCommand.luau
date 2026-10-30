--!nonstrict
-- commands/VoteCommand.luau
-- /vote <game> — cast a vote for the next minigame; tab-completes the
-- votable list during the Lobby phase.

local state = require("core/GameState")
local registry = require("core/GameRegistry")
local VoteBook = require("core/VoteBook")

return {
    name = "vote <game:word>",
    help = "Vote for the next minigame",
    suggest = {
        game = function()
            return state.phase == "Lobby" and registry:votable() or {}
        end,
    },
    handler = function(p, args)
        VoteBook.cast(p, args.game)
    end,
}
