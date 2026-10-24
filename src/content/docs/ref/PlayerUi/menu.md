---
title: 'playerUi.menu'
description: 'A titled grid of up to 54 items over the player''s view; each pick is answered by on_pick(player, n)'
---

Part of [`playerUi`](/ref/PlayerUi/).

```luau
playerUi.menu(opts: { title: Text ?, items: { ItemSpec }, on_pick: (player: Player, n: number) -> (), on_close: ((player: Player) -> ())?, }) → Menu
```

A titled grid of up to 54 items over the player's view; each pick is answered by `on_pick(player, n)`. Nothing goes in or out of it: the items are pictures, not stacks. A chest on Java, a form of buttons on Bedrock. `on_close` fires when the player puts it away without picking. A new menu replaces the open one.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `opts` | `{ title: Text ?, items: { ItemSpec }, on_pick: (player: Player , n: number ) -> (), on_close: ((player: Player ) -> ())?, }` | yes |

## Returns

- [`Menu`](/ref/Menu/)
