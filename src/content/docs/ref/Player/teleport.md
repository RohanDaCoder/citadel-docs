---
title: 'player:teleport'
description: 'Yaw and pitch left out keep the way they face.'
---

Part of [`Player`](/ref/Player/).

```luau
player:teleport(pos: Vec3, rotation: BodyRotation ?)
```

Yaw and pitch left out keep the way they face.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `pos` | [`Vec3`](/ref/Vec3/) | yes |
| `rotation` | [`BodyRotation`](/ref/BodyRotation/) | no |

## Used in

> "player:teleport(world.spawn_point)" — [Guide: Your first pack](/getting-started/quick-start/)
> "not need to repeat its coordinates in the script. `player:teleport` moves" — [Guide: Your first pack](/getting-started/quick-start/)
> "player:teleport(world.spawn_point)" — [Your first pack](/getting-started/quick-start/)
> "`/spawn`, `player:teleport(world.spawn_point)` returns them to the point" — [Your first pack](/getting-started/quick-start/)
> "player:teleport(pos, { yaw = 0, pitch = 0 })   -- a rotation; an angle left out keeps the way they face" — [Players](/players/player-lifecycle/)
> "commands.add("spawn", function(player) player:teleport(SPAWN) end, { aliases = { "hub" } })" — [Commands](/systems/commands/)
