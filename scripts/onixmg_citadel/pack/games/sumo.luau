--!nonstrict
-- games/sumo.luau — shove everyone else off the ring.
--
-- Ported from plugins/Skript/scripts/Games/4_Sumo.sk, which is only the
-- y < -48 void check plus whatever vanilla melee does: on the live server
-- the ring is ordinary punching, damage and all. Here the round loop
-- carries the void check and normal player damage is left alone, so the
-- knockback of every punch is the game.
--
-- (If Citadel's knockback proves too gentle in play, give the shove back:
-- p:push(vec3(dx/dist*0.65, 0.42, dz/dist*0.65)) in an on_damage hook,
-- returning false so the punch does no damage.)

local sumo = {
    name = "Sumo",
    key = "sumo",
    arena = "sumo",
    blurb = "Punch off opponents out of the arena!",   -- the Skript's own wording
    icon = "player_head",
    title_color = "dark_red",   -- "&4&lSumo" in mg_start_game
    votable = false,            -- commented out of {minigames::list::*} on live
    duration = 120,             -- mg_start_game's one timer, every game
    void_y = 69,                -- the Skript's y < -48, lifted by the SHIFT
}

return sumo
