---
title: "ui.row"
description: "The children are the list part: ui.row{ gap = 4, a, b }."
---

Part of [`ui`](/ref/Ui/).

```luau
ui.row(opts: { gap: number ?, align: LayoutAlign ?, [number]: LayoutNode }) → LayoutNode
```

The children are the list part: `ui.row{ gap = 4, a, b }`.

## Parameters

| Name   | Type                                                              | Required |
| ------ | ----------------------------------------------------------------- | -------- |
| `opts` | `{ gap: number ?, align: LayoutAlign ?, [ number ]: LayoutNode }` | yes      |

## Returns

- [`LayoutNode`](/ref/LayoutNode/)

## Used in

> "ui.row{ gap = 6, align = "end"," — [Layouts](/ui/screens/)
> "\| `ui.row{}` \| its children side by side \| `gap`, `align`, then the children \|" — [Layouts](/ui/screens/)
