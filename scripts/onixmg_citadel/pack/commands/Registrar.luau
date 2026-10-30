--!nonstrict
-- commands/Registrar.luau
-- One purpose: register a command spec with Citadel — the single place
-- the shared command plumbing lives (DRY). A spec is a plain table:
--   name     the full pattern, e.g. "vote <game:word>"          (required)
--   handler  function(p, args)                                  (required)
--   help, aliases, suggest  passed straight to commands.add
--   admin    true -> gate behind Perms.is_admin first
--   deny     custom admin denial message (default "You do not
--            have permission.")
--   cooldown seconds -> gate behind Cooldown under "cmd_<word>"
-- The admin gate and the cooldown were copy-pasted across seven commands
-- before; now they are written once, here.

local Perms = require("util/Perms")
local Cooldown = require("commands/Cooldown")

local Registrar = {}

function Registrar.add(spec)
    commands.add(spec.name, function(p, args)
        if spec.admin and not Perms.is_admin(p) then
            return spec.deny or "You do not have permission."
        end
        if spec.cooldown and Cooldown.check(p, "cmd_" .. spec.name:match("^(%S+)"), spec.cooldown) then
            return
        end
        return spec.handler(p, args)
    end, {
        aliases = spec.aliases,
        help = spec.help,
        suggest = spec.suggest,
    })
end

return Registrar
