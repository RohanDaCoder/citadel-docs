---
title: "players.within"
description: "Returns every player inside a box of blocks, corners included."
---

Part of [`players`](/ref/Players/).

```luau
players.within(from: Vec3, to: Vec3) → { Player }
```

Returns every player inside a box of blocks, corners included.

## Parameters

| Name   | Type                 | Required |
| ------ | -------------------- | -------- |
| `from` | [`Vec3`](/ref/Vec3/) | yes      |
| `to`   | [`Vec3`](/ref/Vec3/) | yes      |

## Returns

- `{ Player }`

## Used in

> "players.within(from, to) -- every player inside a box of blocks, corners included" — [Zones and raycasts](/world/spatial-queries/)
