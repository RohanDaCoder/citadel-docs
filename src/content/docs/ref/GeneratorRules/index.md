---
title: "GeneratorRules type"
description: "What world.generate takes"
---

What `world.generate` takes. Without `height` and `density`, the rules add to the land the game's own terrain made.

## Fields

| Field                                                                                                       | Purpose                                                                                                                                                                          |
| ----------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`generatorRules.height: (Field \| number)?`](/ref/GeneratorRules/height/)                                  | The y of the surface.                                                                                                                                                            |
| [`generatorRules.density: Field ?`](/ref/GeneratorRules/density/)                                           | Solid where this is above 0, for caves, overhangs and land in the air.                                                                                                           |
| [`generatorRules.sea: number ?`](/ref/GeneratorRules/sea/)                                                  | Water fills the open air up to this y.                                                                                                                                           |
| [`generatorRules.fluid: string ?`](/ref/GeneratorRules/fluid/)                                              |                                                                                                                                                                                  |
| [`generatorRules.floor: string ?`](/ref/GeneratorRules/floor/)                                              | The block at y 0; "bedrock" for a land of its own.                                                                                                                               |
| [`generatorRules.biomes: { { [number]: string, when: (Field \| number)? } }?`](/ref/GeneratorRules/biomes/) | `{ "desert", when = field }`: the first that holds names the column's biome; one with no `when` is for the rest.                                                                 |
| [`generatorRules.rock: { GroundRule }?`](/ref/GeneratorRules/rock/)                                         | The body of the land, under the ground rules.                                                                                                                                    |
| [`generatorRules.surface: { GroundRule }?`](/ref/GeneratorRules/surface/)                                   |                                                                                                                                                                                  |
| [`generatorRules.plants: { PlantRule }?`](/ref/GeneratorRules/plants/)                                      |                                                                                                                                                                                  |
| [`generatorRules.things: { ThingGrid }?`](/ref/GeneratorRules/things/)                                      |                                                                                                                                                                                  |
| [`generatorRules.fluids: { FluidRule }?`](/ref/GeneratorRules/fluids/)                                      | What fills the caves: needs `density` or `carvers`.                                                                                                                              |
| [`generatorRules.carvers: { "caves" \| "ravines" }?`](/ref/GeneratorRules/carvers/)                         | The game version's own carvers, with the world seed, after the land and before the cave rules: "caves" (every version), "ravines" (b1.8 and later). Needs `height` or `density`. |
| [`generatorRules.structures: { "mineshaft" \| "dungeon" }?`](/ref/GeneratorRules/structures/)               | The game version's own structures, with spawners and loot: "mineshaft", "dungeon" (1.7 to 1.12). Needs `height` or `density`.                                                    |
