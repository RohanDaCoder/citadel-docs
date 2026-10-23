---
title: "world.set_block"
url: /docs/citadel/reference/World/set_block
---

# world.set_block

`skin` is for "player_head" and "player_wall_head" only: an account's name, or the raw `textures` property.

```
world.set_block(pos: Vec3, block: BlockRef, opts: { skin: HeadSkin? }?)
```


## Parameters


## Used in
- [`world.set_block(at, "light_weighted_pressure_plate")`Guide: Coin rush](/docs/citadel/guides/coin-rush)
- [`world.set_block(coin.at, "air")`Guide: Coin rush](/docs/citadel/guides/coin-rush)
- [`(`world.set_block`, `world.fill`) stays in memory.`Server settings](/docs/citadel/server-settings)
- [`world.set_block(pos, block) -- live change, stored and sent to everyone`Blocks and terrain](/docs/citadel/blocks-and-terrain)
- [`world.set_block(pos, "player_head[rotation=8]", { skin = "Notch" }) -- a head with a face; see "player heads"`Blocks and terrain](/docs/citadel/blocks-and-terrain)
- [`- Blocks your script writes are not edits: `world.set_block` from a callback,`Named parts](/docs/citadel/named-parts)
- [`world.set_block(vec3(10, 65, 10), crate) -- the handle, or "rave:crate"`Custom blocks](/docs/citadel/custom-blocks)
- [`like `world.set_block`.`Custom blocks](/docs/citadel/custom-blocks)
