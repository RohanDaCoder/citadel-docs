---
title: "sound global · type Sound"
description: "Plays and stops sounds for everyone in a room: the sound global, or room.sound."
---

Plays and stops sounds for everyone in a room: the `sound` global, or `room.sound`.

Part of the [Sound](/ui/sound/) article.

## Functions

| Call                           | Purpose                                                                                                                                                                                                                                                                                        |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`play`](/ref/Sound/play/)     | Plays a sound by name to everyone in the room; volume above 1 carries further, pitch 0.5..2.0.                                                                                                                                                                                                 |
| [`stop`](/ref/Sound/stop/)     | One sound by name, or every sound, for everyone in the room; 1.13+.                                                                                                                                                                                                                            |
| [`stream`](/ref/Sound/stream/) | A live stream (MP3, or an FLV's sound) or a pack's sound file (OGG, MP3, WAV), heard through the mod a screen's stream uses. With `at`, from speakers: each player hears every speaker within `distance`. Without, from no place, at one volume. `to`: only these players. `loop`: files only. |
