---
title: "Sound"
description: "sound.play and player:sound for short effects through the client's resource pack, sound.stop, and sound.stream — music, ambience and radios through Simple Voice Chat, from speakers that move or no place at all."
---

:::note[In short]
play the game's sounds or the pack's own, for everyone or at a
point. [`sound.play`](/ref/Sound/play/) sends short effects through the
resource pack — no mod needed. [`sound.stream`](/ref/Sound/stream/) plays a
live stream or a pack's sound file through the players' voice mods, with
speakers, moving sources and a list of listeners: music, ambience, radios.
:::

## `sound.play`

```luau
sound.play("block.note_block.hat", { at = player.at, pitch = 1.5 })
sound.play(name, { at = spawn, volume = 1, pitch = 1, category = "record" })
```

- Names are `"<pack>.<file>"` for your assets, or vanilla names like
  `"block.note_block.hat"`.
- Volume above 1 carries further (16 blocks per unit); pitch 0.5..2.0 is two
  octaves.
- `category` is `"record"` (the jukebox slider), `"music"` or `"master"`.
- Every call is one packet to every player, sent ahead of particles.

[`player:sound(name, opts)`](/ref/Player/sound/) plays a sound by name to this
player only, with the same optional position, volume, pitch and category.

## Stopping

```luau
sound.stop("rave.track")   -- stops that sound for everyone in the room
sound.stop()               -- stops every sound
```

`sound.stop` needs 1.13 and later; older clients play on.

## `sound.stream`

`sound.stream` plays a live stream or a pack's sound file through the players'
voice mods, with no screen. A live stream is MP3, as a radio station sends it,
or the sound of an FLV stream. A file is OGG (Vorbis), MP3 or WAV in the pack;
it is decoded while it plays, never loaded whole.

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

| Option          | What it is                                                                                             |
| --------------- | ------------------------------------------------------------------------------------------------------ |
| `url` or `file` | A live stream URL, or a pack sound file (OGG, MP3, WAV). Give one, never both                          |
| `at`            | A vec3, a player, an entity, or a list of them: the speakers                                           |
| `distance`      | 1 to 128 blocks, 48 when not given; needs `at`                                                         |
| `to`            | A player or a list of players; without it, everyone in the room, players who join later too            |
| `loop`          | `true` is for a file only: a live stream has no end, and if it drops it is tried again every 2 seconds |
| `name`          | 1 to 16 characters, `"Sounds"` when not given: the sound's own volume slider in the mod                |

## Speakers

- A speaker that follows a player or entity moves with it, and is silent while
  they are gone. `at = {}` starts with no speakers; `add` gives it some.
- All speakers play the same sound at the same time, as a speaker system does.
  A player hears every speaker in range, each from its own place, and the voice
  mod mixes them. Each one is a packet of its own to that player: three
  speakers in range send three times the sound's data.
- `move`, `add` and `remove` on a sound with no `at` are an error. A sound with
  no place has no distance, and giving one is an error.
- `listen` and `unlisten` change who hears while it plays.

:::caution[Gotcha]
on a stopped sound, every call does nothing. The sound stops with
`stop()`, or when the script stops or reloads.
:::

## The mod

Players hear a stream through Simple Voice Chat: Citadel is a voice server for
it, as a Paper server with the mod's plugin is (UDP port 24454,
`CITADEL_VOICE_PORT`). A player without the mod, or on a client older than
1.13, hears nothing.

A screen can carry the sound itself — an FLV stream's sound, or an MP3 radio
over a pack-drawn picture — with `screen:play{ url = .. }`; see
[Canvases and pictures](/ui/canvases/#streams-and-sound).

## `sound.play` or `sound.stream`

|                           | `sound.play`                                                | `sound.stream`                                                     |
| ------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------ |
| How it reaches the player | The game's or the pack's resource pack; the client plays it | Simple Voice Chat, from the server                                 |
| Mod needed                | No                                                          | Yes                                                                |
| Control                   | Start and stop                                              | Speakers, moving sources, a list of listeners, all players in time |
| Best for                  | Short effects: a click, a door, an alarm                    | Music, ambience, long voice lines, radios, speaker systems         |

## See also

- [Canvases and pictures](/ui/canvases/) — streams and sound through a screen.
- [Particles and lasers](/ui/fx/) — the other room-wide effect, sent after sound.
- [Conventions](/concepts/conventions/) — the `"<pack>.<file>"` sound-name rule.
- [Coin rush guide](/guides/guide-coin-rush/) — `sound.play` in a working pack.
