---
title: "blockSpec.power"
url: /docs/citadel/reference/BlockSpec/power
---

# blockSpec.power

What it gives a redstone circuit, 0 or 15: one number for every face, a table keyed by face (the names `texture` takes), or a list of either with one entry per state. It is the power a block of redstone gives.

```
blockSpec.power: (number | { [string]: number } | { number | { [string]: number } })?
```
