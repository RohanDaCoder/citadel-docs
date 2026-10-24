---
title: "world.puppet"
description: "Places a mob's body with no mind of its own that the script moves; its name tag always shows"
---

Part of [`world`](/ref/World/).

```luau
world.puppet(opts: { kind: string, at: Vec3 ?, rotation: BodyRotation ?, name: Text ? }) → Puppet
```

Places a mob's body with no mind of its own that the script moves; its name tag always shows. An error when this game has no such mob kind.

## Parameters

| Name   | Type                                                                    | Required |
| ------ | ----------------------------------------------------------------------- | -------- |
| `opts` | `{ kind: string , at: Vec3 ?, rotation: BodyRotation ?, name: Text ? }` | yes      |

## Returns

- [`Puppet`](/ref/Puppet/)

## Used in

> "\| A mob appearance moved entirely by the pack \| `world.puppet` \| Uses a mob body without its AI or gameplay simulation. \|" — [Displays](/ui/displays/)
> "local p = world.puppet{ kind = "horse", at = vec3(0.5, 65, -100.5), rotation = { yaw = 90 }, name = { "Lightning", color = "gold" } } -- name is text" — [NPCs](/entities/npcs/)
