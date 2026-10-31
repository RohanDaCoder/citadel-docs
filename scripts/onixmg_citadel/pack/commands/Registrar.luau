--!nonstrict
-- commands/Registrar.luau
-- One purpose: register a command spec with Citadel — the single place
-- the shared command plumbing lives (DRY). Two doors in:
--   Registrar.add(spec)      a standalone command: spec.name is the full
--                            usage line, e.g. "vote <game:word>"
--   Registrar.add_onix(spec) one shape of the grouped /onix command:
--                            spec.usage is the words after "onix", e.g.
--                            "admin game start" or "map state [name:word]"
-- Both doors share one wrapper, so the gates are written once:
--   admin     true -> gate behind Perms.is_admin first
--   deny      custom admin denial message (default "You do not
--             have permission.")
--   cooldown  seconds -> gate behind Cooldown under a key derived from
--             the usage ("onix admin game start" -> cmd_onix_admin_game_start)
--   handler   function(p, args)                                  (required)
--   help, aliases, suggest  passed straight to commands.add
-- The admin gate and the cooldown were copy-pasted across seven commands
-- before; now they are written once, here, for both kinds of command.

local Perms = require("util/Perms")
local Cooldown = require("commands/Cooldown")

local Registrar = {}

-- The cooldown key from a usage line: everything before the first
-- argument, spaces to underscores. "vote <game:word>" -> "cmd_vote";
-- "onix map changemapstate [state:word]" -> "cmd_onix_map_changemapstate".
local function cooldown_key(usage)
    local head = usage:gsub("[%<%[].*$", "")
    head = head:gsub("^%s+", ""):gsub("%s+$", "")
    return "cmd_" .. head:gsub("%s+", "_")
end

-- The one wrapper every spec runs through: admin gate, cooldown, handler.
local function wrap(spec, usage)
    return function(p, args)
        if spec.admin and not Perms.is_admin(p) then
            return spec.deny or "You do not have permission."
        end
        if spec.cooldown and Cooldown.check(p, cooldown_key(usage), spec.cooldown) then
            return
        end
        return spec.handler(p, args)
    end
end

function Registrar.add(spec)
    commands.add(spec.name, wrap(spec, spec.name), {
        aliases = spec.aliases,
        help = spec.help,
        suggest = spec.suggest,
    })
end

function Registrar.add_onix(spec)
    -- "" is the bare /onix line that lists the tree (OnixTree registers
    -- it last, after every real shape, so a line always fits the most
    -- specific shape first).
    local usage = (spec.usage == "" and "onix") or ("onix " .. spec.usage)
    commands.add(usage, wrap(spec, usage), {
        help = spec.help,
        suggest = spec.suggest,
    })
end

return Registrar
