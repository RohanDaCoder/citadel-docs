--!nonstrict
-- games/Game.luau
-- The base class every minigame extends. Carries the shared fields (name,
-- key, arena, blurb, icon, title_colour, duration, void_y, votable) and
-- the default no-op lifecycle hooks the cycle driver calls:
--   onStart, onStep(dt), onStop, onLeave(p), onClick(p, hit), onDamage(victim, hit)
-- Subclasses override the hooks they need and use the shared helpers
-- (broadcastRuns, bumpStat, inRoster, ...) which delegate to the core
-- services, so a game never reaches for a global directly.

local Constants = require("state/Constants")
local Messages = require("core/Messages")
local Stats = require("core/Stats")
local state = require("core/GameState")

local Game = {}
Game.__index = Game

function Game.new(def)
    local self = setmetatable({}, Game)
    self.name = def.name
    self.key = def.key
    self.arena = def.arena
    self.blurb = def.blurb
    self.icon = def.icon
    self.title_color = def.title_color
    self.duration = def.duration or Constants.ROUND_SECONDS
    self.void_y = def.void_y
    self.votable = def.votable ~= false   -- default true
    return self
end

-- Default lifecycle hooks (overridable).
function Game:onStart() end
function Game:onStep(dt) end
function Game:onStop() end
function Game:onLeave(p) end
function Game:onClick(p, hit) end
function Game:onDamage(victim, hit) end

-- Shared helpers for subclasses.
function Game:broadcastRuns(runs)   Messages.broadcast_runs(runs) end
function Game:broadcast(body, col)  Messages.broadcast(body, col) end
function Game:bumpStat(uuid, key)   Stats.bump(uuid, key) end
function Game:inRoster(p)           return state:in_roster(p) end
function Game:roster()              return state.roster end
function Game:phase()               return state.phase end
function Game:discord()             return Constants.DISCORD end

return Game
