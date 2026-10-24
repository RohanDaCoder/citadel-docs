---
title: 'ui.label'
description: 'Words in the client''s own letters, space to ~'
---

Part of [`ui`](/ref/Ui/).

```luau
ui.label(opts: { id: string ?, text: string ?, width: number ?, align: LayoutAlign ?, color: Ink ? }) → LayoutNode
```

Words in the client's own letters, space to `~`. Give a label whose words change a `width`.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `opts` | `{ id: string ?, text: string ?, width: number ?, align: LayoutAlign ?, color: Ink ? }` | yes |

## Returns

- [`LayoutNode`](/ref/LayoutNode/)

## Used in

> "ui.label{ id = "hp_text", text = "20 / 20", width = 82 }," — [Layouts](/ui/screens/)
> "ui.label{ id = "level", text = "1", color = "gold" }," — [Layouts](/ui/screens/)
