--!nonstrict
-- commands/ChangeMapStateCommand.luau
-- /changemapstate [state] — admin. With a state name, paste it directly
-- (no reply, the clicker sent to spawn, exactly as the Skript had it);
-- without, open the map-state picker. Refused mid-game.

local state = require("core/GameState")
local Arena = require("core/Arena")
local Sidebar = require("ui/Sidebar")
local MapStatesMenu = require("ui/menus/MapStatesMenu")

return {
    name = "changemapstate [state:word]",
    help = "Open the map state picker, or paste a state directly",
    admin = true,
    suggest = { state = function() return Arena:maps() end },
    handler = function(p, args)
        if state.phase == "Ingame" then
            return "The map cannot change during a game."
        end
        if args.state then
            if not Arena:show(args.state) then
                return "No map state named " .. args.state .. "."
            end
            Arena:send(p, "lobby")   -- the Skript's spawn() after the click
            Sidebar.refresh()
        else
            MapStatesMenu.open(p)
        end
    end,
}
