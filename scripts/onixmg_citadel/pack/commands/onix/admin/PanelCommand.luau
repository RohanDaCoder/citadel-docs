--!nonstrict
-- commands/onix/admin/PanelCommand.luau
-- /onix admin panel — open the admin panel (the old /adminpanel; the
-- panel's own perm gate stays as it was).

local AdminMenu = require("ui/menus/AdminMenu")

return {
    usage = "admin panel",
    help = "Open the admin panel",
    admin = true,
    handler = function(p)
        AdminMenu.open(p)
    end,
}
