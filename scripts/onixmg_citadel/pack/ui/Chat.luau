--!nonstrict
-- ui/Chat.luau
-- The chat renderer: LPC's "{prefix}{name}: {message}" format, the
-- prefix being the player's LuckPerms group tag. The default group never
-- had one; admins get the owner gradient small-caps tag. The default
-- rendering is replaced (return false).

local Perms = require("util/Perms")

local Chat = {}

-- LuckPerms' owner tag, letter for letter:
--   "&r&8[&#cf0ab9&lᴏ&#d71ea3&lᴡ&#e0328e&lɴ&#e84678&lᴇ&#f05a62&lʀ&8] &r"
local function owner_tag()
    return {
        { "[", color = "dark_gray" },
        { "ᴏ", color = color(207 / 255, 10 / 255, 185 / 255), bold = true },
        { "ᴡ", color = color(215 / 255, 30 / 255, 163 / 255), bold = true },
        { "ɴ", color = color(224 / 255, 50 / 255, 142 / 255), bold = true },
        { "ᴇ", color = color(232 / 255, 70 / 255, 120 / 255), bold = true },
        { "ʀ", color = color(240 / 255, 90 / 255, 98 / 255), bold = true },
        { "] ", color = "dark_gray" },
    }
end

function Chat.render(p, text)
    local runs = {}
    if Perms.is_admin(p) then
        for _, run in owner_tag() do table.insert(runs, run) end
    end
    table.insert(runs, { p.name })
    table.insert(runs, { ": " })
    table.insert(runs, { text })
    message(runs)
    return false
end

return Chat
