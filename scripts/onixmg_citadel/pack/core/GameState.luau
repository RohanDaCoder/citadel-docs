--!nonstrict
-- core/GameState.luau
-- The single shared round-state object. Holds the phase clock, roster,
-- vote tallies, generation counter and the cycle-waiter coroutine, with
-- pure query/mutator methods. Cross-subsystem behaviour (announcing
-- votes, eliminating players, driving the loop) lives in VoteBook,
-- CycleDriver and the games; this is just the data they share.
--
-- One instance exists for the whole pack; subsystems require this module
-- and call its methods on the returned singleton.

local GameState = {}
GameState.__index = GameState

function GameState:reset_for_loading()
    self.phase = "Loading"
    self.active = nil
    self.roster = {}
    self.timer = 0
end

function GameState:reset_votes()
    self.votes = {}
    self.voted = {}
end

function GameState:vote_count(name)
    return self.votes[name] or 0
end

function GameState:has_voted(p)
    return self.voted[p] == true
end

function GameState:record_vote(p, name)
    self.voted[p] = true
    self.votes[name] = self:vote_count(name) + 1
end

function GameState:in_roster(p)
    for _, v in self.roster do
        if v == p then return true end
    end
    return false
end

function GameState:leave_roster(p)
    for i, v in self.roster do
        if v == p then
            table.remove(self.roster, i)
            return true
        end
    end
    return false
end

function GameState:add_to_roster(p)
    table.insert(self.roster, p)
end

function GameState:clear_roster()
    self.roster = {}
end

function GameState:bump_gen()
    self.gen = self.gen + 1
    return self.gen
end

function GameState:set_timer(n)
    self.timer = math.floor(n)
    self.timer_override = math.floor(n)
end

function GameState:take_waiter()
    local w = self.cycle_waiter
    self.cycle_waiter = nil
    return w
end

local state = setmetatable({
    phase = "Disabled",   -- Loading | Lobby | Ingame | Result | Disabled
    active = nil,         -- the running game's name
    timer = 0,
    timer_override = nil, -- /settimer and the panel's clock land here; the
                          -- countdown loops consume it as the new remaining
    roster = {},
    votes = {},
    voted = {},
    gen = 0,
    running = false,
    skip = false,
    cycle_waiter = nil,   -- the coroutine parked in Loading when the server
                          -- is empty; resumed by onJoin (a player joined) or
                          -- by stop (gen bumped), so the loop never polls
}, GameState)

return state
