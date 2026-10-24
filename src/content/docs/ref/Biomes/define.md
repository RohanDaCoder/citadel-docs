---
title: "biomes.define"
description: 'Defines a biome, or changes the one of that name, and returns its full name ("mypack:crystal")'
---

Part of [`biomes`](/ref/Biomes/).

```luau
biomes.define(def: BiomeDefinition) → string
```

Defines a biome, or changes the one of that name, and returns its full name ("mypack:crystal"). Call it at the top of the script: a player learns the biomes when they join.

## Parameters

| Name  | Type                                       | Required |
| ----- | ------------------------------------------ | -------- |
| `def` | [`BiomeDefinition`](/ref/BiomeDefinition/) | yes      |

## Returns

- `string`

## Used in

> "local crystal = game.biomes.define {" — [Blocks and terrain](/world/terrain-generation/)
