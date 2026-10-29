---
title: 'plantRule.place'
description: 'Where it goes: "top" (the default), or in the caves density or carvers dig: "floor", "ceiling" (it hangs down: tip is lowest) or "wall" (one block; {wall} in its name is the side the rock is on, {faci'
---

Part of [`plantRule`](/ref/PlantRule/).

```luau
plantRule.place: ("top" | "floor" | "ceiling" | "wall")?
```

Where it goes: "top" (the default), or in the caves `density` or `carvers` dig: "floor", "ceiling" (it hangs down: `tip` is lowest) or "wall" (one block; `{wall}` in its name is the side the rock is on, `{facing}` the side away). One plant on each floor and each ceiling of a cave, and in each wall block. `when` and `chance` are read at the air block it starts in.
