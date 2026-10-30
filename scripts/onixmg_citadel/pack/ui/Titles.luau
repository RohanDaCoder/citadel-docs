--!nonstrict
-- ui/Titles.luau
-- Title/subtitle cues: the round's "Loading..." and the winner card.

local Text = require("util/Text")

local Titles = {}

function Titles.loading()
    ui.title{ title = "", subtitle = "Loading...", color = "gray", stay = 2 }
end

function Titles.winner(name_runs)
    ui.title{
        title = { "WINNER!", color = "yellow", bold = true },
        subtitle = Text.cat(name_runs, { { " won the game!", color = "yellow" } }),
        stay = 5,
    }
end

return Titles
