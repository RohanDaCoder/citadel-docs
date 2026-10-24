---
title: 'routes.add'
description: 'From one dimension to another: standing ticks ticks in block, or only by player:travel without a trigger; arriving at placement or the destination''s spawn.'
---

Part of [`routes`](/ref/routes/).

```luau
routes.add(route: { from: string, to: string, trigger: { block: string, ticks: number ? }?, placement: Vec3 ? })
```

From one dimension to another: standing `ticks` ticks in `block`, or only by `player:travel` without a trigger; arriving at `placement` or the destination's spawn.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `route` | `{ from: string , to: string , trigger: { block: string , ticks: number ? }?, placement: Vec3 ? }` | yes |

## Used in

> "routes.add{" — [Guide: A dungeon dimension](/guides/guide-a-dungeon-dimension/)
> "routes.add{ from = "overworld", to = "dungeon", trigger = { block = "light_blue_carpet", ticks = 1 }, placement = { x = 0.5, y = 65, z = 0.5 } }" — [Dimensions](/concepts/rooms-and-dimensions/)
> "routes.add{ from = "dungeon", to = "overworld" }  -- no trigger: only player:travel takes it" — [Dimensions](/concepts/rooms-and-dimensions/)
