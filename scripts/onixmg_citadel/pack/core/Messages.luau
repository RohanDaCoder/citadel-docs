--!nonstrict
-- core/Messages.luau
-- Chat messaging: the OnixMG prefix, the debug prefix, and the tell /
-- broadcast / deny / discord helpers built on them. Every colour is the
-- live server's own; the prefix runs are reused by the cycle, the games
-- and the menus so no message diverges from the original.

local Constants = require("state/Constants")
local Text = require("util/Text")
local Sound = require("util/Sound")

local Messages = {}

local function prefix_runs()
    return {
        { "Onix", color = Constants.ONIX, bold = true },
        { "MG", color = Constants.MG, bold = true },
        { " | ", color = "dark_gray" },
    }
end

-- sendDebug's prefix: "<#aa0000><b>ᴅᴇʙᴜɢ <#555555>|<reset>"
local function debug_prefix_runs()
    return {
        { "ᴅᴇʙᴜɢ", color = Constants.DEBUG_RED, bold = true },
        { " | ", color = "dark_gray" },
    }
end

Messages.cat = Text.cat
Messages.prefix_runs = prefix_runs

function Messages.tell(p, body, col)
    p:message(Text.cat(prefix_runs(), { { body, color = col or "white" } }))
end

function Messages.broadcast(body, col)
    message(Text.cat(prefix_runs(), { { body, color = col or "white" } }))
end

-- The prefix + already-built runs: for two-tone messages such as
-- "&eSelected Game: &a&lSpleef".
function Messages.broadcast_runs(runs)
    message(Text.cat(prefix_runs(), runs))
end

function Messages.debug(body)
    for _, p in players.list() do
        if p:has("onix.debug") then
            p:message(Text.cat(debug_prefix_runs(), { { body, color = "white" } }))
        end
    end
end

function Messages.deny(p, body)
    Messages.tell(p, body, "red")
    Sound.deny(p)
end

function Messages.deny_runs(p, runs)
    p:message(Text.cat(prefix_runs(), runs))
    Sound.deny(p)
end

-- The Discord line: green text, blue underlined link. Citadel chat cannot
-- open URLs, so the address is the message. With a player, just to them;
-- without, to everyone.
function Messages.discord_broadcast(p)
    local text = {
        { "Join our discord server! ", color = "green" },
        { Constants.DISCORD, color = "blue", underline = true },
    }
    if p then p:message(text) else message(text) end
end

return Messages
