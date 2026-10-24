---
title: 'menu:update'
description: 'New pictures in place, the menu left open: a bar that fills, a count that changes'
---

Part of [`Menu`](/ref/Menu/).

```luau
menu:update(items: { ItemSpec }) → boolean
```

New pictures in place, the menu left open: a bar that fills, a count that changes. `on_pick` still answers by position. `false` once the player has put it away; a Bedrock form keeps what it showed.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `items` | `{ ItemSpec }` | yes |

## Returns

- `boolean`

## Used in

> "- `menu:update` returns `false` after the player closes the menu. Picks still answer by position. A Bedrock form keeps its first items." — [Menus](/ui/menus/)
