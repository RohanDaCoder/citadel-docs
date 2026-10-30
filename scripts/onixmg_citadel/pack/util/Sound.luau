--!nonstrict
-- util/Sound.luau
-- Named sound cues. Citadel's volume 1 is full volume (the live Skript's
-- "volume 10" was its own loudness trick), so every cue here uses 1
-- unless a quieter one is wanted. Centralising them keeps the exact
-- sound/pitch pairs the live server used in one place.

local Sound = {}

function Sound.deny(p)                 -- anvil land, the deny pair
    p:sound("block.anvil.land", { volume = 1, pitch = 1 })
end
function Sound.bass()                  -- vote skip / system stop
    sound.play("block.note_block.bass", { volume = 1, pitch = 1 })
end
function Sound.levelup()               -- round start
    sound.play("entity.player.levelup", { volume = 1, pitch = 1 })
end
function Sound.toast()                 -- winner
    sound.play("ui.toast.challenge_complete", { volume = 1, pitch = 1 })
end
function Sound.lava()                  -- elimination
    sound.play("block.lava.extinguish", { volume = 1, pitch = 1 })
end
function Sound.bit(pitch, vol)         -- vote countdown tick / discord broadcast
    sound.play("block.note_block.bit", { volume = vol or 1, pitch = pitch or 1 })
end
function Sound.pling(p, pitch)         -- vote cast
    p:sound("block.note_block.pling", { volume = 1, pitch = pitch or 2 })
end

return Sound
