---
title: "generatorRules.biomes"
url: /docs/citadel/reference/GeneratorRules/biomes
---

# generatorRules.biomes

`{ "desert", when = field }`: the first that holds names the column's biome; one with no `when` is for the rest.

```
generatorRules.biomes: { { [number]: string, when: (Field | number)? } }?
```
