---
title: 'entities.define'
description: 'Load time only'
---

Part of [`entities`](/ref/Entities/).

```luau
entities.define(spec: EntitySpec) → EntityDef
```

Load time only. A definition is a fact about the world.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `spec` | [`EntitySpec`](/ref/EntitySpec/) | yes |

## Returns

- [`EntityDef`](/ref/EntityDef/)

## Used in

> "\| Physics, gameplay hooks or persistence \| `game.entities.define` and `world.spawn` \| Gives a body behavior independent of its appearance. \|" — [Displays](/ui/displays/)
> "local car = game.entities.define {" — [Displays](/ui/displays/)
> "local rocket = game.entities.define {" — [Custom entities](/entities/custom-entities/)
> "local sheep = game.entities.define {" — [Custom entities](/entities/custom-entities/)
> "in `game.entities.define`, which answers `"take"` or `"ignore"`." — [Cancelling events](/concepts/events/)
