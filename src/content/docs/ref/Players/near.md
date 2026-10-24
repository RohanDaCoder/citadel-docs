---
title: "players.near"
description: "Who is within a radius of a point, and who is inside a box of blocks."
---

Part of [`players`](/ref/Players/).

```luau
players.near(pos: Vec3, radius: number) → { Player }
```

Who is within a radius of a point, and who is inside a box of blocks.

## Parameters

| Name     | Type                 | Required |
| -------- | -------------------- | -------- |
| `pos`    | [`Vec3`](/ref/Vec3/) | yes      |
| `radius` | `number`             | yes      |

## Returns

- `{ Player }`

## Used in

> "players.near(pos, 8) -- every player within eight blocks of a point" — [Zones and raycasts](/world/spatial-queries/)
