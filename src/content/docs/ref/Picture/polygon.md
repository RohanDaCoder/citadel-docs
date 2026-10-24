---
title: 'picture:polygon'
description: 'Fills a smoothed shape with any number of corners; a point is {x, y} or { x = .., y = .'
---

Part of [`Picture`](/ref/Picture/).

```luau
picture:polygon(points: { { number } | { x: number, y: number } }, color: Ink)
```

Fills a smoothed shape with any number of corners; a point is `{x, y}` or `{ x = .., y = .. }`.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `points` | `{ { number } \| { x: number , y: number } }` | yes |
| `color` | [`Ink`](/ref/Ink/) | yes |
