--!nonstrict
-- commands/AdminPanelCommand.luau
-- /adminpanel (+ ap) — open the admin panel.

local AdminMenu = require("ui/menus/AdminMenu")

return {
    name = "adminpanel",
    aliases = { "ap" },
    help = "Open the admin panel",
    handler = function(p)
        AdminMenu.open(p)
    end,
}
