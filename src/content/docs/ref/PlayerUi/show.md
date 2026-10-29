---
title: 'playerUi.show'
description: 'Puts a layout on this player''s screen'
---

Part of [`playerUi`](/ref/PlayerUi/).

```luau
playerUi.show(layout: Layout) → Hud
```

Puts a layout on this player's screen. A client older than 1.21.4 (`player:supports("layout")`) gets a handle that shows nothing.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `layout` | [`Layout`](/ref/Layout/) | yes |

## Returns

- [`Hud`](/ref/Hud/)
