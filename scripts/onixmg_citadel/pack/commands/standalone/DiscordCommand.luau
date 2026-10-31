--!nonstrict
-- commands/standalone/DiscordCommand.luau
-- /discord (+ dc, dcserver, discordserver, onixdiscord) — the Discord
-- line and the soft note.

local Messages = require("core/Messages")

return {
    name = "discord",
    aliases = { "dc", "dcserver", "discordserver", "onixdiscord" },
    help = "Join the official discord server",
    handler = function(p)
        Messages.discord_broadcast(p)
        p:sound("entity.experience_orb.pickup", { volume = 0.5, pitch = 1 })
    end,
}
