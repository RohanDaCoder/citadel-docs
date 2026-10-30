--!nonstrict
-- core/GameRegistry.luau
-- The registered games and the votable list. `order` is the votable list
-- as the live server's variables built it (Spleef and TNT Run votable;
-- Sumo and Hot Potato stayed commented out, registered with votable =
-- false). all() walks every registered game in the canonical order the
-- profile uses.

local Constants = require("state/Constants")

local GameRegistry = {}
GameRegistry.__index = GameRegistry

function GameRegistry:register(game)
    self.games[game.name] = game
    if game.votable ~= false then
        table.insert(self.order, game.name)
    end
end

function GameRegistry:get(name)
    return self.games[name]
end

function GameRegistry:votable()
    return self.order
end

function GameRegistry:all()
    local out = {}
    for _, name in Constants.GAME_ORDER do
        if self.games[name] then table.insert(out, name) end
    end
    return out
end

local registry = setmetatable({ games = {}, order = {} }, GameRegistry)
return registry
