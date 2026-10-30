--!nonstrict
-- tasks/DiscordBroadcastTask.luau
-- One purpose: the two-minute Discord announcement — the link and the
-- soft note, whenever anyone is online to hear it.

local Messages = require("core/Messages")

local DiscordBroadcastTask = {}

function DiscordBroadcastTask.start()
    task.spawn(function()
        while true do
            task.wait(120)
            if players.count() > 0 then
                Messages.discord_broadcast()
                sound.play("block.note_block.bit", { volume = 0.3, pitch = 1.5 })
            end
        end
    end)
end

return DiscordBroadcastTask
