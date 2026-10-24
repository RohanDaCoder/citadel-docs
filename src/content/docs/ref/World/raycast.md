---
title: "world.raycast"
description: "The first block a ray from from along direction meets within max blocks, and the face it came in through; nil for none."
---

Part of [`world`](/ref/World/).

```luau
world.raycast(from: Vec3, direction: Vec3, max: number ?) → RayHit ?
```

The first block a ray from `from` along `direction` meets within `max` blocks, and the face it came in through; nil for none.

## Parameters

| Name        | Type                 | Required |
| ----------- | -------------------- | -------- |
| `from`      | [`Vec3`](/ref/Vec3/) | yes      |
| `direction` | [`Vec3`](/ref/Vec3/) | yes      |
| `max`       | `number`             | no       |

## Returns

- [`RayHit`](/ref/RayHit/)

## Used in

> "world.raycast(from, direction, 32) -- the first block a ray meets within 32 blocks, or nil:" — [Zones and raycasts](/world/spatial-queries/)
> "world.raycast(player.at + vec3(0, 1.62, 0), player:look()) -- what the player is looking at" — [Zones and raycasts](/world/spatial-queries/)
