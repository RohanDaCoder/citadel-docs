---
title: "chunk:fill"
url: /docs/citadel/reference/Chunk/fill
---

# chunk:fill

Fills a box of blocks, clipped to the chunk.

```
chunk:fill(from: Vec3, to: Vec3, block: string)
```


## Parameters


## Used in
- [`chunk:fill(`Guide: Your first pack](/docs/citadel/guides/your-first-pack)
- [``chunk:fill` fills the box between two corners, including both corners.`Guide: Your first pack](/docs/citadel/guides/your-first-pack)
- [`chunk:fill(vec3(-3, 64, -3), vec3(3, 64, 3), "quartz_block") -- clipped to the chunk`Guide: Parkour, a room each](/docs/citadel/guides/parkour-a-room-each)
- [``chunk:fill` with corners outside the chunk is clipped to it, so one line`Guide: Parkour, a room each](/docs/citadel/guides/parkour-a-room-each)
- [`chunk:fill(vec3(chunk.min.x, 63, chunk.min.z), vec3(chunk.max.x, 63, chunk.max.z), "dirt")`Guide: Build a cottage](/docs/citadel/guides/build-a-cottage)
- [`chunk:fill(vec3(chunk.min.x, 64, chunk.min.z), vec3(chunk.max.x, 64, chunk.max.z), "grass_block")`Guide: Build a cottage](/docs/citadel/guides/build-a-cottage)
- [`chunk:fill(vec3(chunk.min.x, 64, chunk.min.z), vec3(chunk.max.x, 64, chunk.max.z), "stone_bricks")`Guide: A dungeon dimension](/docs/citadel/guides/a-dungeon-dimension)
- [`chunk:fill(vec3(4, 65, 4), vec3(5, 65, 5), "light_blue_carpet")`Guide: A dungeon dimension](/docs/citadel/guides/a-dungeon-dimension)
