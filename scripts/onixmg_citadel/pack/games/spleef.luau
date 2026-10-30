--!nonstrict
-- games/spleef.luau — dig the snow out from under everyone.
--
-- Ported from plugins/Skript/scripts/Games/1_Spleef.sk:
--   * "/si give spleef_shovel" gave every player a shovel; the /si plugin
--     is gone from the live server, so here a glinted shovel is placed in
--     the hotbar and the script does the digging
--   * "on player move: y < -48" is the round loop's void check (void_y)
--   * the old "on command /spawn" case — running /spawn during Spleef
--     eliminated the runner — is /spawn's own job in main.luau, for every
--     game the Skript gave a y-check to

local spleef = {
    name = "Spleef",
    key = "spleef",
    arena = "spleef",
    blurb = "Dig your way to victory!",
    icon = "golden_shovel",
    title_color = "yellow",   -- "&e&lSpleef" in mg_start_game
    duration = 120,            -- mg_start_game's one timer, every game
    void_y = 69,               -- the Skript's y < -48, lifted by the SHIFT
}

local DIGGABLE = {
    snow_block = true,
    snow = true,
    snow_layer = true,
}

function spleef.start()
    for _, p in players.list() do
        p:hotbar{
            [1] = {
                item = "golden_shovel",
                name = "Spleef Shovel",
                lore = { "Left click the snow" },
                glint = true,
            },
        }
    end
end

function spleef.on_click(p, hit)
    if hit.button ~= "left" or not hit.block then return end

    local block = world.get_block(hit.block)
    if not block or not DIGGABLE[block] then return end

    world.set_block(hit.block, "air")
    p:sound("block.snow.break", { at = hit.block, volume = 0.8, pitch = 1 })
end

return spleef
