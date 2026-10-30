--!nonstrict
-- commands/ProfileCommand.luau
-- /profile [player] — your stats page, or another player's.

local ProfileMenu = require("ui/menus/ProfileMenu")

return {
    name = "profile [target:player]",
    help = "Your stats, or another player's",
    handler = function(p, args)
        ProfileMenu.open(p, args.target or p)
    end,
}
