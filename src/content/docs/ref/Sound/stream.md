---
title: "sound.stream"
description: "A live stream (MP3, or an FLV's sound) or a pack's sound file (OGG, MP3, WAV), heard through the mod a screen's stream uses"
---

Part of [`sound`](/ref/Sound/).

```luau
sound.stream(opts: { url: string ?, file: string ?, at: (SoundSpeaker | { SoundSpeaker })?, to: (Player | { Player })?, distance: number ?, loop: boolean ?, name: string ?, }) → SoundStream
```

A live stream (MP3, or an FLV's sound) or a pack's sound file (OGG, MP3, WAV), heard through the mod a screen's stream uses. With `at`, from speakers: each player hears every speaker within `distance`. Without, from no place, at one volume. `to`: only these players. `loop`: files only.

## Parameters

| Name   | Type                                                                                                                                                              | Required |
| ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| `opts` | `{ url: string ?, file: string ?, at: ( SoundSpeaker \| { SoundSpeaker })?, to: ( Player \| { Player })?, distance: number ?, loop: boolean ?, name: string ?, }` | yes      |

## Returns

- [`SoundStream`](/ref/SoundStream/)

## Used in

> "[`sound.stream`](#sound)." — [Canvases](/ui/canvases/)
> "## sound.stream" — [Sound](/ui/sound/)
> "`sound.stream` plays a live stream or a pack's sound file through the" — [Sound](/ui/sound/)
