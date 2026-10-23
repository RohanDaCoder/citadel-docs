---
title: 'world.screen'
description: 'Puts a wall of map frames, width by height frames (128 pixels each), in front of a wall; at is the top-left frame'
---

Part of [`world`](/ref/World/).

```luau
world.screen(opts: { at: Vec3, facing: Facing | "up", up: Facing ?, width: number ?, height: number ?, glow: boolean ?, on_click: ((player: Player, x: number, y: number, button: "left" | "right") -> ())?, }) → Screen
```

Puts a wall of map frames, `width` by `height` frames (128 pixels each), in front of a wall; `at` is the top-left frame. Returns a Screen.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `opts` | `{ at: Vec3 , facing: Facing \| "up" , up: Facing ?, width: number ?, height: number ?, glow: boolean ?, on_click: ((player: Player , x: number , y: number , button: "left" \| "right" ) -> ())?, }` | yes |

## Returns

- [`Screen`](/ref/Screen/)

## Used in

> "local board = world.screen{ at = vec3(-2, 68, -10), facing = "south", width = 4, height = 2 }" — [Scoreboard with a button](/guides/guide-scoreboard-with-a-button/)
> "local board = world.screen{ at = vec3(-2, 68, -10), facing = "south", width = 4, height = 2 }" — [Screens](/ui/screens/)
> "Set `on_click` (in `world.screen{}` or later) to get the pixel a player" — [Screens](/ui/screens/)
> "local tv = world.screen{ at = vec3(-2, 70, -9), facing = "south", width = 4, height = 2 }" — [Canvases](/ui/canvases/)
