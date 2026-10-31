--!nonstrict
-- ui/menus/VoteMenu.luau
-- One purpose: the vote menu — one glinted card per votable game, with
-- the live count, re-opened after every pick. The cards center in a
-- chest the kit sizes to fit; a pick comes back as the game's name.

local state = require("core/GameState")
local registry = require("core/GameRegistry")
local VoteBook = require("core/VoteBook")
local kit = require("ui/MenuKit")

local VoteMenu = {}

function VoteMenu.open(p)
    local cards = {}
    for _, name in registry:votable() do
        local g = registry:get(name)
        local votes = state:vote_count(name)
        table.insert(cards, {
            key = name,
            item = g.icon or "paper",
            name = { { name, color = g.title_color or "yellow", bold = true } },
            lore = {
                g.blurb or "",
                votes .. (votes == 1 and " vote" or " votes"),
                "Click to vote",
            },
            count = math.max(votes, 1),
            glint = true,
        })
    end

    kit.menu(p, {
        title = { { "Vote for the next game", color = "yellow", bold = true } },
        content = { { items = cards, spacing = 1 } },
        on_pick = function(who, key)
            VoteBook.cast(who, key)
            VoteMenu.open(who)
        end,
    })
end

return VoteMenu
