---
title: 'world.fill'
description: 'Fills a box of blocks between two corners, live, stored and sent to everyone.'
---

Part of [`world`](/ref/World/).

```luau
world.fill(from: Vec3, to: Vec3, block: BlockRef)
```

Fills a box of blocks between two corners, live, stored and sent to everyone.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `from` | [`Vec3`](/ref/Vec3/) | yes |
| `to` | [`Vec3`](/ref/Vec3/) | yes |
| `block` | [`BlockRef`](/ref/BlockRef/) | yes |

## Used in

> "(`world.set_block`, `world.fill`) stays in memory." — [Server settings](/systems/server-settings/)
> "world.fill(from, to, block)               -- live box" — [Blocks and terrain](/world/terrain-generation/)
> "world.paste(schem, origin)                -- live, like world.fill; { part = "house" } names the paste" — [Blocks and terrain](/world/terrain-generation/)
