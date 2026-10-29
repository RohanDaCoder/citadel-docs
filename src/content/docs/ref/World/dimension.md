---
title: 'world.dimension'
description: 'Another world of the server''s group, by dimension id or its last part ("dungeon", "minecraft:the_nether"): that world''s own world table.'
---

Part of [`world`](/ref/World/).

```luau
world.dimension(name: string) → World
```

Another world of the server's group, by dimension id or its last part ("dungeon", "minecraft:the_nether"): that world's own `world` table.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `name` | `string` | yes |

## Returns

- [`World`](/ref/World/)

## Used in

> "`world.dimension(name)` is that world's own `world` table. Its" — [Guide: A dungeon dimension](/guides/guide-a-dungeon-dimension/)
> "local dungeon = world.dimension("dungeon")" — [Guide: A dungeon dimension](/guides/guide-a-dungeon-dimension/)
> "local dungeon = world.dimension("dungeon")    -- that world's `world` table; "minecraft:the_nether" works too" — [Dimensions](/concepts/rooms-and-dimensions/)
