---
title: 'world.build'
description: 'The same value, written in code instead of read from a file'
---

Part of [`world`](/ref/World/).

```luau
world.build(fn: (b: Builder) -> (), opts: { detail: number ? }?) → Schematic
```

The same value, written in code instead of read from a file. `{ detail = 2 }`: coordinates are half blocks, fitted to slabs and stairs.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `fn` | `(b: Builder ) -> ()` | yes |
| `opts` | `{ detail: number ? }` | no |

## Returns

- [`Schematic`](/ref/Schematic/)

## Used in

> "`world.build` makes a build in code: a schematic with no file. It gets a" — [Guide: Build a cottage](/guides/guide-build-a-cottage/)
> "local cottage = world.build(function(b)" — [Guide: Build a cottage](/guides/guide-build-a-cottage/)
> "world.build(function(b) end, { detail = 1 })   -- the same value, written in code; detail 2 is half blocks" — [Blocks and terrain](/world/terrain-generation/)
> "local road = world.build(function(b)" — [Blocks and terrain](/world/terrain-generation/)
> "detail = 1,                        -- as world.build: 1, or 2 for half blocks" — [Named parts](/world/building/)
> "build = function(b) ... end,       -- exactly a world.build function" — [Named parts](/world/building/)
