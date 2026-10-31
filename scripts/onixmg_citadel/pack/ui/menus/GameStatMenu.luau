--!nonstrict
-- ui/menus/GameStatMenu.luau
-- One purpose: one game's stat page — games played, wins, the game icon
-- and the per-game extra (blocks broken for TNT Run, potato touches for
-- Hot Potato), with Back to the game list. The stat cards are display;
-- only the Back line acts.

local Stats = require("core/Stats")
local kit = require("ui/MenuKit")

local GameStatMenu = {}

function GameStatMenu.open(viewer, target, g)
    local uuid = target.uuid
    local played = Stats.stat(uuid, "played." .. g.key)
    local wins = Stats.stat(uuid, "wins." .. g.key)

    local cards = {
        { item = "book", name = "Games Played", lore = { tostring(played) } },
        { item = "diamond", name = "Wins", lore = { tostring(wins) } },
        kit.game_icon(g),
    }
    if g.key == "tntrun" then
        table.insert(cards, { item = "tnt", name = "Blocks Broken", lore = { tostring(Stats.stat(uuid, "tntrun")) } })
    elseif g.key == "hotpotato" then
        table.insert(cards, { item = "blaze_powder", name = "Potato Touches", lore = { tostring(Stats.stat(uuid, "hotpotato_touches")) } })
    end

    kit.menu(viewer, {
        title = {
            { g.name, color = "gray", bold = true },
            { " - ", color = "gray" },
            { target.name, color = "white" },
        },
        rows = 3,
        content = { { items = cards, spacing = 1 } },
        back = "Return to game list",
        on_pick = function(who, key)
            if key == "back" then
                -- Required lazily: back-link to the game list, which
                -- top-level-requires this file.
                require("ui/menus/GameListMenu").open(who, target)
            end
        end,
    })
end

return GameStatMenu
