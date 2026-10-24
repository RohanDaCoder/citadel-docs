---
title: 'world.on_entity_death'
description: 'Tells after a mob died; it is gone, so its id and name is all there is'
---

Part of [`world`](/ref/World/).

```luau
world.on_entity_death(fn: (id: number, name: string) -> ()) → Connection
```

Tells after a mob died; it is gone, so its id and name is all there is. Mob kinds only.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `fn` | `(id: number , name: string ) -> ()` | yes |

## Returns

- [`Connection`](/ref/Connection/)

## Used in

> "- At 0 health it dies as a mob: it falls over, leaves its `drops`, and is gone a second later. `on_remove` gets `"killed"`, and `world.on_entity_death` fires." — [Custom entities](/entities/custom-entities/)
> "world.on_entity_death(function(id, name) end) -> connection    -- a mob died; it is gone, so id and name is all there is" — [Game events](/concepts/events/)
> "`world.on_entity_spawn` fires for mob kinds only. `world.on_entity_death`" — [Game events](/concepts/events/)
