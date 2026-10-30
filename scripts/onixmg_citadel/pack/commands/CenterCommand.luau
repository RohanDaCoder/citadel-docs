--!nonstrict
-- commands/CenterCommand.luau
-- /center [yaw] [pitch] — admin. Snap to the centre of the current
-- block, keep the current angles unless given, with the yellow
-- confirmation and the teleport chime.

local Messages = require("core/Messages")

return {
    name = "center [yaw:number] [pitch:number]",
    help = "Snap to the centre of your block",
    admin = true,
    deny = "You do not have permission to center yourself.",
    suggest = {
        yaw = { "0", "90", "180", "-90" },
        pitch = { "0", "90", "-90" },
    },
    handler = function(p, args)
        local at = p.at
        local rot = p.rotation
        p:teleport(
            vec3(math.floor(at.x) + 0.5, math.floor(at.y), math.floor(at.z) + 0.5),
            { yaw = args.yaw or rot.yaw, pitch = args.pitch or rot.pitch }
        )
        Messages.tell(p, "You have been centered!", "yellow")
        p:sound("entity.enderman.teleport", { volume = 0.5, pitch = 2 })
    end,
}
