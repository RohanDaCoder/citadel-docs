# SOURCE: Sound

## sound.stream
`sound.stream` plays a live stream or a pack’s sound file through the
players’ voice mods, with no screen. A live stream is MP3, as a radio station
sends it, or the sound of an FLV stream. A file is OGG (Vorbis), MP3 or WAV in
the pack; it is decoded while it plays, never loaded whole.
```luau
-- 3D: from speakers. Each player hears every speaker within `distance`.
local radio = sound.stream{ url = "https://radio.example.org/live.mp3", at = vec3(10, 67, 28), distance = 24 }
local pa = sound.stream{ url = url, at = { vec3(10, 67, 28), vec3(-10, 67, 28), captain }, distance = 16 }
local hum = sound.stream{ file = "assets/music/engine.ogg", at = engine_room, loop = true }

-- No place: the same volume for each listener, no fade, no direction.
sound.stream{ url = url }                         -- everyone in the room
sound.stream{ file = "assets/voice/welcome.mp3", to = player }
sound.stream{ url = url, to = { p1, p2 }, name = "Radio" }

radio.playing            -- false once stopped, or once a file that does not loop ends
pa:move(2, vec3(-12, 67, 30))   -- speakers are numbered from 1
pa:add(npc)                     -- a speaker that follows a player or an entity; gives its number
pa:remove(3)
radio:listen(player)            -- starts to hear it
radio:unlisten(player)          -- stops hearing it
radio:stop()
```
- Give `url` or `file`, never both. `loop = true` is for a file only: a live
stream has no end, and if it drops it is tried again every 2 seconds.
- `at` is a vec3, a player, an entity, or a list of them. A speaker that
follows a player or entity moves with it, and is silent while they are
gone. `at = {}` starts with no speakers; `add` gives it some.
- All speakers play the same sound at the same time, as a speaker system
does. A player hears every speaker in range, each from its own place, and
the voice mod mixes them. Each one is a packet of its own to that player:
three speakers in range send three times the sound’s data.
- `distance` is 1 to 128 blocks, 48 when not given. It needs `at`: a sound
with no place has no distance, and giving one is an error.
- `to` is a player or a list of players. Without it, everyone in the room
hears the sound, players who join later too. `listen` and `unlisten`
change who hears while it plays.
- `name` (1 to 16 characters, `"Sounds"` when not given) is the sound’s own
volume slider in the mod.
- `move`, `add` and `remove` on a sound with no `at` are an error. On a
stopped sound, every call does nothing.
- The sound stops with `stop()`, or when the script stops or reloads.
- Players hear it through Simple Voice Chat, as a screen’s stream: a player
without the mod, or on a client older than 1.13, hears nothing.
|  | `sound.play` | `sound.stream` |
| --- | --- | --- |
| How it reaches the player | The game’s or the pack’s resource pack; the client plays it | Simple Voice Chat, from the server |
| Mod needed | No | Yes |
| Control | Start and stop | Speakers, moving sources, a list of listeners, all players in time |
| Best for | Short effects: a click, a door, an alarm | Music, ambience, long voice lines, radios, speaker systems |
