---
title: "world.container"
description: "A chest's stacks, or nil where the block keeps none."
---

Part of [`world`](/ref/World/).

```luau
world.container(pos: Vec3) → Container ?
```

A chest's stacks, or nil where the block keeps none.

## Parameters

| Name  | Type                 | Required |
| ----- | -------------------- | -------- |
| `pos` | [`Vec3`](/ref/Vec3/) | yes      |

## Returns

- [`Container`](/ref/Container/)

## Used in

> "world.container(pos) -- a chest's stacks, or nil; see "containers"" — [Blocks and terrain](/world/terrain-generation/)
> "local box = world.container(pos) -- nil unless the block there is a chest" — [Blocks and terrain](/world/terrain-generation/)
> "- A chest's stacks are `world.container` (see "containers")." — [Players](/players/player-lifecycle/)
