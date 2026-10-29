---
title: 'player:has'
description: 'True if the player''s groups give them this permission node; operators have every node.'
---

Part of [`Player`](/ref/Player/).

```luau
player:has(node: string) → boolean
```

True if the player's groups give them this permission node; operators have every node.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `node` | `string` | yes |

## Returns

- `boolean`

## Used in

> "player:has("casino.vip")         -- true" — [Permissions](/players/permissions/)
> "- Gate your own commands with `player:has`." — [Permissions](/players/permissions/)
