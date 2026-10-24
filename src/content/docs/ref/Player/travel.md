---
title: "player:travel"
description: "Sends the player to another world of the group, at pos or its spawn."
---

Part of [`Player`](/ref/Player/).

```luau
player:travel(dimension: string, pos: Vec3 ?)
```

Sends the player to another world of the group, at `pos` or its spawn.

## Parameters

| Name        | Type                 | Required |
| ----------- | -------------------- | -------- |
| `dimension` | `string`             | yes      |
| `pos`       | [`Vec3`](/ref/Vec3/) | no       |

## Used in

> "`player:travel(dimension, pos)` sends a player to any world of the group, at" — [Guide: A dungeon dimension](/guides/guide-a-dungeon-dimension/)
> "player:travel("overworld")" — [Guide: A dungeon dimension](/guides/guide-a-dungeon-dimension/)
> "routes.add{ from = "dungeon", to = "overworld" } -- no trigger: only player:travel takes it" — [Dimensions](/concepts/rooms-and-dimensions/)
> "player:travel("dungeon", vec3(0.5, 65, 0.5)) -- to a point, or without one to its spawn" — [Dimensions](/concepts/rooms-and-dimensions/)
