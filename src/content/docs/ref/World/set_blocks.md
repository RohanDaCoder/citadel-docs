---
title: 'world.set_blocks'
description: 'Sets many blocks at once, live, stored and sent; the cheapest way'
---

Part of [`world`](/ref/World/).

```luau
world.set_blocks(changes: { { at: Vec3, block: BlockRef, skin: HeadSkin ? } })
```

Sets many blocks at once, live, stored and sent; the cheapest way. A row takes `skin` too, for a player head.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `changes` | `{ { at: Vec3 , block: BlockRef , skin: HeadSkin ? } }` | yes |

## Used in

> "world.set_blocks({ { at = vec3(...), block = "red_wool" }, ... })   -- many at once, cheapest; a row takes skin = too" — [Blocks and terrain](/world/terrain-generation/)
> "world.set_blocks({ { at = vec3(3, 65, 0), block = "player_head", skin = "jeb_" } })" — [Blocks and terrain](/world/terrain-generation/)
