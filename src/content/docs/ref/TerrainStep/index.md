---
title: "TerrainStep type"
description: "One populate step of the overworld, as citadel.yml writes it, read from game.terrain.steps."
---

One populate step of the overworld, as citadel.yml writes it, read from `game.terrain.steps`.

## Fields

| Field                                                        | Purpose                                                                                                   |
| ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| [`terrainStep.step: string`](/ref/TerrainStep/step/)         | Which populate step: "dungeons", "clay", "ore", "trees", "patch", "reeds", "cactus", "springs" or "snow". |
| [`terrainStep.block: string ?`](/ref/TerrainStep/block/)     | The block a clay, ore or patch step places.                                                               |
| [`terrainStep.fluid: string ?`](/ref/TerrainStep/fluid/)     | The fluid a springs step places: "water" or "lava".                                                       |
| [`terrainStep.count: number ?`](/ref/TerrainStep/count/)     | How many tries, veins, blobs, clumps or springs the step makes in a chunk.                                |
| [`terrainStep.size: number ?`](/ref/TerrainStep/size/)       | How long each clay blob or ore vein is.                                                                   |
| [`terrainStep.below: number ?`](/ref/TerrainStep/below/)     | An ore step places its veins below this y.                                                                |
| [`terrainStep.bonus: number ?`](/ref/TerrainStep/bonus/)     | Trees: one chunk in this many gets one more tree.                                                         |
| [`terrainStep.big: number ?`](/ref/TerrainStep/big/)         | Trees: one chunk in this many grows big trees instead of small ones.                                      |
| [`terrainStep.chance: number ?`](/ref/TerrainStep/chance/)   | Patch: made one time in this many, in place of `count` times.                                             |
| [`terrainStep.bound: number ?`](/ref/TerrainStep/bound/)     | Springs: the y is picked below this bound before `nesting` pushes it deeper.                              |
| [`terrainStep.nesting: number ?`](/ref/TerrainStep/nesting/) | Springs: how many times the y is picked again below itself; lava's 2 keeps it deeper than water's 1.      |
