--!nonstrict
-- commands/Commands.luau
-- One purpose: the pack's command catalog — the standalone player
-- commands (one file each in standalone/) plus the /onix command tree
-- (one file per leaf in onix/), every one registered through the shared
-- Registrar. Adding a command means adding its one file and one line in
-- the list it belongs to.

local Registrar = require("commands/Registrar")
local OnixTree = require("commands/onix/OnixTree")

local Commands = {}

-- Player-facing commands that stay outside the /onix tree, exactly as on
-- the live server: the vote is the lobby's one-key verb, /spawn is the
-- way out of a round, /discord /list /profile are everyone's info lines.
local STANDALONE = {
    require("commands/standalone/VoteCommand"),
    require("commands/standalone/SpawnCommand"),
    require("commands/standalone/DiscordCommand"),
    require("commands/standalone/ListCommand"),
    require("commands/standalone/ProfileCommand"),
}

function Commands.register()
    for _, spec in STANDALONE do
        Registrar.add(spec)
    end
    OnixTree.register()
end

return Commands
