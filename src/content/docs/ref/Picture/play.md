---
title: 'picture:play'
description: 'Plays a raw RGB video file from the pack at fps 0.5 to 20, the engine drawing each frame; returns the Video.'
---

Part of [`Picture`](/ref/Picture/).

```luau
picture:play(opts: { file: string, fps: number ?, loop: boolean ? }) → Video
```

Plays a raw RGB video file from the pack at `fps` 0.5 to 20, the engine drawing each frame; returns the Video.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `opts` | `{ file: string , fps: number ?, loop: boolean ? }` | yes |

## Returns

- [`Video`](/ref/Video/)
