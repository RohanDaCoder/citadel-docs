---
title: "player:travel"
url: /docs/citadel/reference/Player/travel
---

# player:travel

Sends the player to another world of the group, at `pos` or its spawn.

```
player:travel(dimension: string, pos: Vec3?)
```


## Parameters


## Used in
- [``player:travel(dimension, pos)` sends a player to any world of the group, at`Guide: A dungeon dimension](/docs/citadel/guides/a-dungeon-dimension)
- [`player:travel("overworld")`Guide: A dungeon dimension](/docs/citadel/guides/a-dungeon-dimension)
- [`routes.add{ from = "dungeon", to = "overworld" } -- no trigger: only player:travel takes it`Dimensions](/docs/citadel/dimensions)
- [`player:travel("dungeon", vec3(0.5, 65, 0.5)) -- to a point, or without one to its spawn`Dimensions](/docs/citadel/dimensions)
