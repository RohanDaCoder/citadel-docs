---
title: 'screen.on_click'
description: 'Called with the pixel the player points at and the button, when a player clicks the screen'
---

Part of [`screen`](/ref/Screen/).

```luau
screen.on_click(((player: Player, x: number, y: number, button: "left" | "right") -> ()) | false) → ?
```

Called with the pixel the player points at and the button, when a player clicks the screen. nil or false takes the hook off.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `((player` | `Player , x: number , y: number , button: "left" \| "right" ) -> ()) \| false` | yes |

## Returns

- `?`
