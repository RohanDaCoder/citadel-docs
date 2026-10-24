---
title: "canvas:view"
description: "The map id of its top-left map, for a filled_map"
---

Part of [`Canvas`](/ref/Canvas/).

```luau
canvas:view(player: Player) → View
```

The map id of its top-left map, for a `filled_map`. Returns that player's own layer over the canvas, drawn with the same calls; only they see it.

## Parameters

| Name     | Type                     | Required |
| -------- | ------------------------ | -------- |
| `player` | [`Player`](/ref/Player/) | yes      |

## Returns

- [`View`](/ref/View/)
