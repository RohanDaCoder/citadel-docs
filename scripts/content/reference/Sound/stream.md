---
title: "sound.stream"
url: /docs/citadel/reference/Sound/stream
---

# sound.stream

A live stream (MP3, or an FLV's sound) or a pack's sound file (OGG, MP3, WAV), heard through the mod a screen's stream uses. With `at`, from speakers: each player hears every speaker within `distance`. Without, from no place, at one volume. `to`: only these players. `loop`: files only.

```
sound.stream(opts: { url: string?, file: string?, at: (SoundSpeaker | { SoundSpeaker })?, to: (Player | { Player })?, distance: number?, loop: boolean?, name: string?, }) → SoundStream
```


## Parameters


## Returns


## Used in
- [`[`sound.stream`](#sound).`Canvases](/docs/citadel/canvases)
- [`## sound.stream`Sound](/docs/citadel/sound)
- [``sound.stream` plays a live stream or a pack's sound file through the`Sound](/docs/citadel/sound)
