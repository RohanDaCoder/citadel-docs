---
title: "world.set_blocks"
url: /docs/citadel/reference/World/set_blocks
---

# world.set_blocks

Sets many blocks at once, live, stored and sent; the cheapest way. A row takes `skin` too, for a player head.

```
world.set_blocks(changes: { { at: Vec3, block: BlockRef, skin: HeadSkin? } })
```


## Parameters


## Used in
- [`world.set_blocks({ { at = vec3(...), block = "red_wool" }, ... }) -- many at once, cheapest; a row takes skin = too`Blocks and terrain](/docs/citadel/blocks-and-terrain)
- [`world.set_blocks({ { at = vec3(3, 65, 0), block = "player_head", skin = "jeb_" } })`Blocks and terrain](/docs/citadel/blocks-and-terrain)
