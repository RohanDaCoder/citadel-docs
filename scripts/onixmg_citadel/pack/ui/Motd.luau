--!nonstrict
-- ui/Motd.luau
-- Essentials' four gold welcome lines (sent on join). The world-time line
-- uses Citadel's world.time() formatted to 12-hour, as the placeholder did.

local Motd = {}

local function world_time12()
    local t = world.time()
    if type(t) ~= "number" then return "6:00 AM" end
    local h = math.floor(t / 1000 + 6) % 24
    local m = math.floor((t % 1000) / 1000 * 60)
    local h12 = h % 12
    if h12 == 0 then h12 = 12 end
    return string.format("%d:%02d %s", h12, m, h < 12 and "AM" or "PM")
end

function Motd.welcome(p)
    p:message({
        { "Welcome, ", color = "gold" },
        { p.name, color = "gold" },
        { "!", color = "gold" },
    })
    p:message({
        { "Type ", color = "gold" },
        { "/help", color = "red" },
        { " for a list of commands.", color = "gold" },
    })
    p:message({
        { "Type ", color = "gold" },
        { "/list", color = "red" },
        { " to see who else is online.", color = "gold" },
    })
    p:message({
        { "Players online: ", color = "gold" },
        { tostring(players.count()), color = "red" },
        { " - World time: ", color = "gold" },
        { world_time12(), color = "red" },
    })
end

return Motd
