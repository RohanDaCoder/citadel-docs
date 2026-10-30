--!nonstrict
-- commands/SpawnCommand.luau
-- /spawn [player] (alias /hub) — the 3-second cooldown with its
-- remaining-time message, admins may send someone else, and the sender
-- goes to spawn at the end either way — eliminated if mid-round, since
-- /spawn was the Spleef Skript's way out of a round.

local state = require("core/GameState")
local Messages = require("core/Messages")
local Eliminator = require("core/Eliminator")
local Lobby = require("core/Lobby")
local Perms = require("util/Perms")

return {
    name = "spawn [target:player]",
    aliases = { "hub" },
    help = "Return to spawn",
    handler = function(p, args)
        -- Custom cooldown: not a silent gate, but the remaining-time line.
        local now = time.now()
        local last = p.data.spawn_last or -100
        if now - last < 3 then
            Messages.tell(p, string.format(
                "Please wait %d seconds before using /spawn again.",
                math.ceil(3 - (now - last))), "red")
            return
        end
        p.data.spawn_last = now

        if args.target and args.target ~= p then
            if not Perms.is_admin(p) then
                Messages.tell(p, "Only administrators can teleport other players.", "red")
                return
            end
            Lobby.send(args.target)
            p:message({
                { "You have teleported ", color = "gray" },
                { args.target.name, color = "white" },
                { " to spawn.", color = "gray" },
            })
        end

        -- and spawn(player), whatever else happened above
        if state.phase == "Ingame" and state:in_roster(p) then
            Eliminator:eliminate(p)
        else
            Lobby.send(p)
        end
    end,
}
