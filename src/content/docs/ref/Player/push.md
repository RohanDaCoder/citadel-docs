---
title: "player:push"
description: "A shove in blocks per tick, on top of what they are doing."
---

Part of [`Player`](/ref/Player/).

```luau
player:push(velocity: Vec3)
```

A shove in blocks per tick, on top of what they are doing.

## Parameters

| Name       | Type                 | Required |
| ---------- | -------------------- | -------- |
| `velocity` | [`Vec3`](/ref/Vec3/) | yes      |

## Used in

> "player:push(vec3(0, 1, 0)) -- a shove, in blocks per tick, on top of what they are doing" — [Body and movement](/players/movement/)
> "- `player:push` and a movement effect (`speed`, `jump_boost`, `levitation`, `slow_falling`, `dolphins_grace`) exempt the player while they last. `player:teleport` is always allowed." — [Room rules](/world/world-state/)
> "hit.player:push(player:look() * 0.5 + vec3(0, 0.3, 0))" — [Room rules](/world/world-state/)
