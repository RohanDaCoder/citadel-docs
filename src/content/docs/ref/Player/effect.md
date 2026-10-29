---
title: 'player:effect'
description: 'A potion effect by its modern name; duration in seconds, math.huge for ever.'
---

Part of [`Player`](/ref/Player/).

```luau
player:effect(name: string, opts: { level: number ?, duration: number ?, particles: boolean ? }?)
```

A potion effect by its modern name; `duration` in seconds, math.huge for ever.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `name` | `string` | yes |
| `opts` | `{ level: number ?, duration: number ?, particles: boolean ? }` | no |

## Used in

> "player:effect("speed", { level = 2, duration = 30, particles = false })" — [Body and movement](/players/movement/)
> "--   `player:effect("mining_fatigue", { level = 5 })` so no block cracks" — [Input](/players/movement/)
