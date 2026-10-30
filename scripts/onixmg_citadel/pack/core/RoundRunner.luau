--!nonstrict
-- core/RoundRunner.luau
-- One purpose: run ONE round of a game, start to stop — roster everyone,
-- paste the arena, teleport the roster, drive the game's lifecycle hooks
-- (onStart/onStep/onStop), apply the per-game void check, keep the timer,
-- sidebar and action bar current, and end on time or when one player is
-- left standing.

local Constants = require("state/Constants")
local state = require("core/GameState")
local registry = require("core/GameRegistry")
local Arena = require("core/Arena")
local Stats = require("core/Stats")
local Sidebar = require("ui/Sidebar")
local ActionBar = require("ui/ActionBar")
local Titles = require("ui/Titles")
local Sound = require("util/Sound")
local Lobby = require("core/Lobby")
local Eliminator = require("core/Eliminator")

local RoundRunner = {}

function RoundRunner:run(name, gen)
    local game = registry:get(name)
    if not game then return end

    state.phase = "Ingame"
    state.active = name
    state:clear_roster()

    Sound.levelup()
    Titles.loading()

    -- Everyone playing is rostered, counted and sent to the lobby point
    -- first, adventure mode included.
    for _, p in players.list() do
        state:add_to_roster(p)
        p.gamemode = 2
        p.health = 20
        Arena:send(p, "lobby")
        Stats.bump(p.uuid, "played")
        Stats.bump(p.uuid, "played." .. game.key)
    end

    Arena:show(game.arena)
    task.wait(3)

    -- "&e&lSpleef &8- &fDig your way to victory!" — a plain broadcast, no
    -- prefix, each game in its own colour.
    message({
        { name, color = game.title_color or "yellow", bold = true },
        { " - ", color = "dark_gray" },
        { game.blurb or "", color = "white" },
    })
    local spawn = Arena:spawn(game.arena)
    local yaw = Arena:yaw(game.arena)
    for _, p in state.roster do
        p:teleport(spawn, { yaw = yaw, pitch = 0 })
    end

    game:onStart()

    local remaining = game.duration or Constants.ROUND_SECONDS
    local acc = 0
    state.timer = math.ceil(remaining)
    Sidebar.refresh()

    while state.gen == gen and remaining > 0 and #state.roster > 1 do
        if state.timer_override then
            remaining = state.timer_override
            state.timer_override = nil
        end
        local dt = task.wait(0.05)
        remaining = remaining - dt

        game:onStep(dt)

        if game.void_y then
            for i = #state.roster, 1, -1 do
                local p = state.roster[i]
                local at = p.at
                if at and at.y < game.void_y then Eliminator:eliminate(p) end
            end
        end

        acc = acc + dt
        if acc >= 0.25 then
            acc = 0
            state.timer = math.max(math.ceil(remaining), 0)
            Sidebar.refresh()
            ActionBar.active(name, state.timer)
        end
    end

    game:onStop()
end

return RoundRunner
