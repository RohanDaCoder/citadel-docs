--!nonstrict
-- ui/Hotbar.luau
-- The lobby hotbar: Vote compass, Profile book, Discord paper. Set on
-- join, on respawn, on round end, and as the non-potato holder's bar in
-- Hot Potato.

local Constants = require("state/Constants")

local Hotbar = {}

function Hotbar.lobby(p)
    p:hotbar{
        [1] = { item = "compass", name = "Vote", lore = { "Choose the next game" } },
        [2] = { item = "book", name = "Profile", lore = { "Your stats" } },
        [5] = { item = "paper", name = "Discord", lore = { Constants.DISCORD } },
    }
end

return Hotbar
