--!nonstrict
-- ui/menus/GameStatMenu.luau
-- One purpose: one game's stat page — games played, wins, the game icon
-- and the per-game extra (blocks broken for TNT Run, potato touches for
-- Hot Potato), with Back to the game list.

local Stats = require("core/Stats")
local kit = require("ui/MenuKit")

local GameStatMenu = {}

function GameStatMenu.open(viewer, target, g)
    local uuid = target.uuid
    local played = Stats.stat(uuid, "played." .. g.key)
    local wins = Stats.stat(uuid, "wins." .. g.key)

    local items = {}
    items[10] = { item = "book", name = "Games Played", lore = { tostring(played) } }
    items[12] = { item = "diamond", name = "Wins", lore = { tostring(wins) } }
    items[13] = kit.game_icon(g)

    if g.key == "tntrun" then
        items[14] = { item = "tnt", name = "Blocks Broken", lore = { tostring(Stats.stat(uuid, "tntrun")) } }
    elseif g.key == "hotpotato" then
        items[14] = { item = "blaze_powder", name = "Potato Touches", lore = { tostring(Stats.stat(uuid, "hotpotato_touches")) } }
    end

    items[16] = kit.back_item("Return to game list")

    kit.open_sound(viewer)
    viewer.ui.menu{
        title = {
            { g.name, color = "gray", bold = true },
            { " - ", color = "gray" },
            { target.name, color = "white" },
        },
        items = kit.pad(items, 3),
        on_pick = function(who, n)
            if n == 16 then
                -- Required lazily: back-link to the game list, which
                -- top-level-requires this file.
                require("ui/menus/GameListMenu").open(who, target)
            end
        end,
    }
end

return GameStatMenu
