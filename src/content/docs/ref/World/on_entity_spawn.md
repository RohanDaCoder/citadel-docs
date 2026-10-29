---
title: 'world.on_entity_spawn'
description: 'Tells after a mob appeared, with its handle and name; a natural spawn fires it on every game version that has one, and a pack''s own world.spawn("cow", pos) fires it too'
---

Part of [`world`](/ref/World/).

```luau
world.on_entity_spawn(fn: (entity: EntityHandle, name: string) -> ()) → Connection
```

Tells after a mob appeared, with its handle and name; a natural spawn fires it on every game version that has one, and a pack's own `world.spawn("cow", pos)` fires it too. Mob kinds only.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `fn` | `(entity: EntityHandle , name: string ) -> ()` | yes |

## Returns

- [`Connection`](/ref/Connection/)

## Used in

> "world.on_entity_spawn(function(entity, name) end) -> connection   -- a mob appeared; entity is the handle" — [Game events](/concepts/events/)
> "`world.on_entity_spawn` fires for mob kinds only. `world.on_entity_death`" — [Game events](/concepts/events/)
