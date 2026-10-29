---
title: "world.get_block"
url: /docs/citadel/reference/World/get_block
---

# world.get_block

`nil` where that chunk is not in memory: a read never generates.

```
world.get_block(pos: Vec3) → string?
```


## Parameters


## Returns


## Used in
- [`while world.get_block(at) ~= "air" do`Guide: Coin rush](/docs/citadel/guides/coin-rush)
- [`while world.get_block(at) ~= "air" do`Guide: Coin rush](/docs/citadel/guides/coin-rush)
- [`world.get_block(pos) -- the block name there, or nil (see below)`Blocks and terrain](/docs/citadel/blocks-and-terrain)
- [`local here = world.get_block(player.at - vec3(0, 1, 0)) -- "grass_block"`Blocks and terrain](/docs/citadel/blocks-and-terrain)
