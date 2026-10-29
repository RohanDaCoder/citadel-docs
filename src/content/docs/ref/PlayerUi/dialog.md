---
title: 'playerUi.dialog'
description: 'A screen of boxes, words and pictures (see "Dialogs"): a ui.kit.window{}, or a function that returns one and is drawn again after every click'
---

Part of [`playerUi`](/ref/PlayerUi/).

```luau
playerUi.dialog(view: DialogNode | () -> DialogNode) → Dialog ?
```

A screen of boxes, words and pictures (see "Dialogs"): a `ui.kit.window{}`, or a function that returns one and is drawn again after every click. nil where `player:supports("dialog")` is false.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `view` | `DialogNode \| () -> DialogNode` | yes |

## Returns

- [`Dialog`](/ref/Dialog/)
