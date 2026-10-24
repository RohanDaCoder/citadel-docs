---
title: "SoundStream type"
description: "A sound sound.stream plays"
---

A sound `sound.stream` plays. Speakers are numbered from 1.

## Functions

| Call                                     | Purpose                                                               |
| ---------------------------------------- | --------------------------------------------------------------------- |
| [`stop`](/ref/SoundStream/stop/)         |                                                                       |
| [`move`](/ref/SoundStream/move/)         | Speakers, for a sound made with `at`; on one with no place, an error. |
| [`add`](/ref/SoundStream/add/)           |                                                                       |
| [`remove`](/ref/SoundStream/remove/)     |                                                                       |
| [`listen`](/ref/SoundStream/listen/)     | Who hears it, changed while it plays.                                 |
| [`unlisten`](/ref/SoundStream/unlisten/) |                                                                       |

## Fields

| Field                                                       | Purpose                                                           |
| ----------------------------------------------------------- | ----------------------------------------------------------------- |
| [`soundStream.playing: boolean`](/ref/SoundStream/playing/) | False once stopped, or once a file that does not loop has played. |
