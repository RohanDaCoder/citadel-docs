---
title: 'hub.point'
description: 'Turns the player''s own live portal to another published experience.'
---

Part of [`hub`](/ref/hub/).

```luau
hub.point(player: Player | string, slot: number, experience: string) → boolean
```

Turns the player's own live portal to another published experience.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `player` | `Player \| string` | yes |
| `slot` | `number` | yes |
| `experience` | `string` | yes |

## Returns

- `boolean`

## Used in

> "- `hub.point(player, slot, experience)` turns the player's own live portal to another published experience, as often as they like. It returns whether it did." — [Hub](/systems/hub/)
