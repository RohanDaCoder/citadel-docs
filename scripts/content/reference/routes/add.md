---
title: "routes.add"
url: /docs/citadel/reference/routes/add
---

# routes.add

From one dimension to another: standing `ticks` ticks in `block`, or only by `player:travel` without a trigger; arriving at `placement` or the destination's spawn.

```
routes.add(route: { from: string, to: string, trigger: { block: string, ticks: number? }?, placement: Vec3? })
```


## Parameters


## Used in
- [`routes.add{`Guide: A dungeon dimension](/docs/citadel/guides/a-dungeon-dimension)
- [`routes.add{ from = "overworld", to = "dungeon", trigger = { block = "light_blue_carpet", ticks = 1 }, placement = { x = 0.5, y = 65, z = 0.5 } }`Dimensions](/docs/citadel/dimensions)
- [`routes.add{ from = "dungeon", to = "overworld" } -- no trigger: only player:travel takes it`Dimensions](/docs/citadel/dimensions)
