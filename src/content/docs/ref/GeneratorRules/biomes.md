---
title: "generatorRules.biomes"
description: '{ "desert", when = field }: the first that holds names the column''s biome; one with no when is for the rest.'
---

Part of [`generatorRules`](/ref/GeneratorRules/).

```luau
generatorRules.biomes: { { [number]: string, when: (Field | number)? } }?
```

`{ "desert", when = field }`: the first that holds names the column's biome; one with no `when` is for the rest.
