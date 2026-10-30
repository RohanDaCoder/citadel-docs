--!nonstrict
-- core/VoteBook.luau
-- Vote tallying and broadcast. The votable list comes from the registry;
-- the tallies live on GameState. announce() prints the whole list with a
-- plain [VOTE] token (Citadel chat cannot run commands; the vote compass
-- and /vote cover the click). cast() validates, records, re-announces,
-- tells the voter and refreshes the sidebar. winning() takes the highest
-- count, the first game in list order on ties; with no votes it picks at
-- random and says so.

local state = require("core/GameState")
local registry = require("core/GameRegistry")
local Messages = require("core/Messages")
local Sound = require("util/Sound")
local Sidebar = require("ui/Sidebar")

local VoteBook = {}

function VoteBook.count(name)
    return state:vote_count(name)
end

function VoteBook.announce()
    message("")
    message({ { "VOTE FOR THE NEXT MINIGAME!", color = "gold", bold = true } })
    for _, name in registry:votable() do
        message({
            { "[VOTE]", color = "green", bold = true },
            { " ", color = "white" },
            { name, color = "white" },
            { " (" .. state:vote_count(name) .. " votes)", color = "gray" },
        })
    end
    message({
        { "Use ", color = "gray" },
        { "/vote", color = "yellow" },
        { " or click ", color = "gray" },
        { "[VOTE]", color = "green", bold = true },
    })
    message("")
end

function VoteBook.cast(p, name)
    if state.phase ~= "Lobby" then
        Messages.deny(p, "No voting in progress!")
        return false
    end
    if state:has_voted(p) then
        Messages.deny(p, "You already voted!")
        return false
    end
    local g = registry:get(name)
    if not g or not table.find(registry:votable(), name) then
        Messages.deny(p, "Invalid game!")
        return false
    end

    state:record_vote(p, name)
    VoteBook.announce()
    p:message(Messages.cat(Messages.prefix_runs(), {
        { "You voted for ", color = "green" },
        { name, color = "white" },
        { "!", color = "green" },
    }))
    Messages.debug(p.name .. " voted for " .. name)
    Sound.pling(p, 2)
    Sidebar.refresh()
    return true
end

-- The highest count wins, the first game in list order taking ties; with
-- no votes at all a random pick is announced. Returns the game name and
-- whether any votes were cast.
function VoteBook.winning()
    local best, bestn = nil, -1
    for _, name in registry:votable() do
        local n = state:vote_count(name)
        if n > bestn then
            best, bestn = name, n
        end
    end
    if bestn <= 0 then
        local order = registry:votable()
        best = order[math.random(#order)]
        Messages.broadcast_runs({
            { "No votes cast! Randomly picking ", color = "yellow" },
            { best, color = "green", bold = true },
        })
        return best, false
    end
    return best, true
end

return VoteBook
