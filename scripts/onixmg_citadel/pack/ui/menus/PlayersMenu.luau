--!nonstrict
-- ui/menus/PlayersMenu.luau
-- One purpose: the admin panel's players submenu — the roster's heads in
-- a centered grid that wraps to as many rows as the roster needs, Back
-- at the bottom. Each head carries its player as the pick key, so a
-- click opens that player's card directly.

local state = require("core/GameState")
local kit = require("ui/MenuKit")
local PlayerCardMenu = require("ui/menus/PlayerCardMenu")

local PlayersMenu = {}

function PlayersMenu.open(p)
    local heads = {}
    for _, target in state.roster do
        local h = kit.head(target.name)
        h.key = target
        table.insert(heads, h)
    end

    kit.menu(p, {
        title = { { "Players", color = "gray", bold = true } },
        content = kit.grid(heads, 7),
        back = "Return to admin panel",
        on_pick = function(who, key)
            if key == "back" then
                -- Required lazily: back-link to the admin panel.
                require("ui/menus/AdminMenu").open(who)
            else
                PlayerCardMenu.open(who, key)
            end
        end,
    })
end

return PlayersMenu
