---
title: "world.build"
url: /docs/citadel/reference/World/build
---

# world.build

The same value, written in code instead of read from a file. `{ detail = 2 }`: coordinates are half blocks, fitted to slabs and stairs.

```
world.build(fn: (b: Builder) -> (), opts: { detail: number? }?) → Schematic
```


## Parameters


## Returns


## Used in
- [``world.build` makes a build in code: a schematic with no file. It gets a`Guide: Build a cottage](/docs/citadel/guides/build-a-cottage)
- [`local cottage = world.build(function(b)`Guide: Build a cottage](/docs/citadel/guides/build-a-cottage)
- [`world.build(function(b) end, { detail = 1 }) -- the same value, written in code; detail 2 is half blocks`Blocks and terrain](/docs/citadel/blocks-and-terrain)
- [`local road = world.build(function(b)`Blocks and terrain](/docs/citadel/blocks-and-terrain)
- [`detail = 1, -- as world.build: 1, or 2 for half blocks`Named parts](/docs/citadel/named-parts)
- [`build = function(b) ... end, -- exactly a world.build function`Named parts](/docs/citadel/named-parts)
