---
title: "world.hitbox"
description: "Makes an invisible box a player can click; solid also makes it a wall"
---

Part of [`world`](/ref/World/).

```luau
world.hitbox(opts: { at: Vec3, width: number ?, height: number ?, depth: number ?, solid: boolean ?, on_click: ((player: Player, button: "left" | "right") -> ())?, }) → Hitbox
```

Makes an invisible box a player can click; `solid` also makes it a wall. `depth` is the width unless given. 1.19.4 and later.

## Parameters

| Name   | Type                                                                                                                                                     | Required |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| `opts` | `{ at: Vec3 , width: number ?, height: number ?, depth: number ?, solid: boolean ?, on_click: ((player: Player , button: "left" \| "right" ) -> ())?, }` | yes      |

## Returns

- [`Hitbox`](/ref/Hitbox/)

## Used in

> "\| `hitbox` \| `world.hitbox` \| 1.19.4 \|" — [Client versions](/appendix/client-versions/)
> "local h = world.hitbox{ at = vec3(...), width = 1, height = 1, on_click = function(player, button) end }" — [Displays](/ui/displays/)
> "`world.hitbox{ ..., solid = true }` is also a **wall**. A player cannot walk" — [Displays](/ui/displays/)
