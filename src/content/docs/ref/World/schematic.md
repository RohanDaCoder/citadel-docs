---
title: "world.schematic"
description: "A file inside the pack; a path that leaves it, or one that is not there, is an error naming the file."
---

Part of [`world`](/ref/World/).

```luau
world.schematic(file: string) → Schematic
```

A file inside the pack; a path that leaves it, or one that is not there, is an error naming the file.

## Parameters

| Name   | Type     | Required |
| ------ | -------- | -------- |
| `file` | `string` | yes      |

## Returns

- [`Schematic`](/ref/Schematic/)

## Used in

> "world.schematic(file) -- a .schem file in the pack, read once" — [Blocks and terrain](/world/terrain-generation/)
> "local town = world.schematic("builds/town.schem")" — [Blocks and terrain](/world/terrain-generation/)
> "`world.schematic` reads. Generating a kept part pastes that file." — [Named parts](/world/building/)
