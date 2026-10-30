--!nonstrict
-- state/Constants.luau
-- Pack-wide constants: the live server's exact colours, prefixes, timings
-- and Discord address. Every colour value is the live Paper server's own
-- (the Onix/MG prefix hex, the debug red, the gradient owner tag) so the
-- chat, tab list and sidebars render identically to it.

local Constants = {}

-- The OnixMG chat prefix, as exact Citadel colour runs:
--   "<#7A8BFA><b>Onix<#204352><b>MG <#555555>|"
Constants.ONIX = color(0x7A / 255, 0x8B / 255, 0xFA / 255)
Constants.MG = color(0x20 / 255, 0x43 / 255, 0x52 / 255)
Constants.DEBUG_RED = color(0xAA / 255, 0, 0)

Constants.ACCENT = "aqua"
Constants.DISCORD = "discord.gg/RyKjZ2pdw2"

-- Round timings (seconds). The round timer is 120s for every game; the
-- vote is 30s; the result cadence is the live server's own.
Constants.VOTE_SECONDS = 30
Constants.ROUND_SECONDS = 120
Constants.RESULT_HOLD = 3      -- winner title before "Returning to lobby..."
Constants.RESULT_RETURN = 7    -- map is lobby; players settle at spawn
Constants.RESULT_GAP = 3       -- "The game has ended!" before the next cycle

-- The four games, in the canonical registration order the profile walks.
Constants.GAME_ORDER = { "Spleef", "TNT Run", "Sumo", "Hot Potato" }

return Constants
