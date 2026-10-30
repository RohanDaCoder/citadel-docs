--!nonstrict
-- ui/menus/VoteMenu.luau
-- One purpose: the vote menu — one glinted card per votable game, with
-- the live count, re-opened after every pick.

local state = require("core/GameState")
local registry = require("core/GameRegistry")
local VoteBook = require("core/VoteBook")
local kit = require("ui/MenuKit")

local VoteMenu = {}

function VoteMenu.open(p)
    local items = {}
    for _, name in registry:votable() do
        local g = registry:get(name)
        local votes = state:vote_count(name)
        table.insert(items, {
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

    kit.open_sound(p)
    p.ui.menu{
        title = { { "Vote for the next game", color = "yellow", bold = true } },
        items = kit.pad(items, 3),
        on_pick = function(who, n)
            local name = registry:votable()[n]
            if name then VoteBook.cast(who, name) end
            VoteMenu.open(who)
        end,
    }
end

return VoteMenu
