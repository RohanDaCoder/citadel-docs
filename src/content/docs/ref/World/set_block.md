---
title: 'world.set_block'
description: 'skin is for "player_head" and "player_wall_head" only: an account''s name, or the raw textures property.'
---

Part of [`world`](/ref/World/).

```luau
world.set_block(pos: Vec3, block: BlockRef, opts: { skin: HeadSkin ? }?)
```

`skin` is for "player_head" and "player_wall_head" only: an account's name, or the raw `textures` property.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `pos` | [`Vec3`](/ref/Vec3/) | yes |
| `block` | [`BlockRef`](/ref/BlockRef/) | yes |
| `opts` | `{ skin: HeadSkin ? }` | no |

## Used in

> "world.set_block(at, "light_weighted_pressure_plate")" — [Guide: Coin rush](/guides/guide-coin-rush/)
> "world.set_block(coin.at, "air")" — [Guide: Coin rush](/guides/guide-coin-rush/)
> "(`world.set_block`, `world.fill`) stays in memory." — [Server settings](/systems/server-settings/)
> "world.set_block(pos, block)               -- live change, stored and sent to everyone" — [Blocks and terrain](/world/terrain-generation/)
> "world.set_block(pos, "player_head[rotation=8]", { skin = "Notch" })   -- a head with a face; see "player heads"" — [Blocks and terrain](/world/terrain-generation/)
> "- Blocks your script writes are not edits: `world.set_block` from a callback," — [Named parts](/world/building/)
