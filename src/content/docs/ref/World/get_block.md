---
title: 'world.get_block'
description: 'nil where that chunk is not in memory: a read never generates.'
---

Part of [`world`](/ref/World/).

```luau
world.get_block(pos: Vec3) → string ?
```

`nil` where that chunk is not in memory: a read never generates.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `pos` | [`Vec3`](/ref/Vec3/) | yes |

## Returns

- `string ?`

## Used in

> "while world.get_block(at) ~= "air" do" — [Guide: Coin rush](/guides/guide-coin-rush/)
> "while world.get_block(at) ~= "air" do" — [Guide: Coin rush](/guides/guide-coin-rush/)
> "world.get_block(pos)                      -- the block name there, or nil (see below)" — [Blocks and terrain](/world/terrain-generation/)
> "local here = world.get_block(player.at - vec3(0, 1, 0))   -- "grass_block"" — [Blocks and terrain](/world/terrain-generation/)
