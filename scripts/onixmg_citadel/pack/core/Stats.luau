--!nonstrict
-- core/Stats.luau
-- Per-player statistics, persisted in Citadel storage under
-- "stats.<uuid>.<key>". The profile and the per-game extras (TNT Run
-- blocks broken, Hot Potato touches) read these; the games and the cycle
-- bump them.

local Stats = {}

function Stats.stat(uuid, key)
    return storage.get("stats." .. uuid .. "." .. key) or 0
end

function Stats.bump(uuid, key)
    storage.set("stats." .. uuid .. "." .. key, Stats.stat(uuid, key) + 1)
end

return Stats
