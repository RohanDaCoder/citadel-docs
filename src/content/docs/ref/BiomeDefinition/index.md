---
title: "BiomeDefinition type"
description: "What a pack changes about the vanilla biome its own biome copies"
---

What a pack changes about the vanilla biome its own biome copies. Each colour is a `Color` or a colour name such as "#7fd8c8".

## Fields

| Field                                                                                              | Purpose                                                                                                        |
| -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| [`biomeDefinition.name: string`](/ref/BiomeDefinition/name/)                                       | Lower case letters, digits and underscores. The pack's name goes in front: "crystal" becomes "mypack:crystal". |
| [`biomeDefinition.like: string ?`](/ref/BiomeDefinition/like/)                                     | The vanilla biome to copy; "plains" when left out.                                                             |
| [`biomeDefinition.grass: (Color \| string)?`](/ref/BiomeDefinition/grass/)                         |                                                                                                                |
| [`biomeDefinition.leaves: (Color \| string)?`](/ref/BiomeDefinition/leaves/)                       |                                                                                                                |
| [`biomeDefinition.water: (Color \| string)?`](/ref/BiomeDefinition/water/)                         |                                                                                                                |
| [`biomeDefinition.water_fog: (Color \| string)?`](/ref/BiomeDefinition/water_fog/)                 | The colour of the view under water.                                                                            |
| [`biomeDefinition.sky: (Color \| string)?`](/ref/BiomeDefinition/sky/)                             |                                                                                                                |
| [`biomeDefinition.fog: (Color \| string)?`](/ref/BiomeDefinition/fog/)                             | The colour of the far distance.                                                                                |
| [`biomeDefinition.weather: ("rain" \| "snow" \| "none" \| false)?`](/ref/BiomeDefinition/weather/) |                                                                                                                |
