--!nonstrict
-- ui/ActionBar.luau
-- Action-bar cues for the vote phase, the last-five-seconds countdown,
-- and the active round. Pure helpers — they take the numbers and build
-- the runs the live server showed.

local ActionBar = {}

-- "&bVoting Phase &8| &eNext game in: &f%timer%s", then
-- "&6&lSTARTING IN &f&l%timer%s" for the last five seconds.
function ActionBar.vote_phase(timer)
    if timer <= 5 then
        ui.actionbar({
            { "STARTING IN ", color = "gold", bold = true },
            { timer .. "s", color = "white", bold = true },
        })
    else
        ui.actionbar({
            { "Voting Phase ", color = "aqua" },
            { "| ", color = "dark_gray" },
            { "Next game in: ", color = "yellow" },
            { timer .. "s", color = "white" },
        })
    end
end

function ActionBar.active(name, timer)
    ui.actionbar({
        { "Active: ", color = "yellow" },
        { name, color = "green" },
        { " | ", color = "dark_gray" },
        { "Remaining: ", color = "yellow" },
        { timer .. "s", color = "white" },
    })
end

function ActionBar.clear()
    ui.actionbar("")
end

return ActionBar
