---
title: "data.remove"
description: "Remove and return a detached value; omitted index removes the last element."
---

Part of [`data`](/ref/data/).

```luau
data.remove(list: DataView, index: number ?) → any
```

Remove and return a detached value; omitted index removes the last element.

## Parameters

| Name    | Type                         | Required |
| ------- | ---------------------------- | -------- |
| `list`  | [`DataView`](/ref/DataView/) | yes      |
| `index` | `number`                     | no       |

## Returns

- `any`

## Used in

> "local last = data.remove(e.data.history) -- removes and returns a detached value" — [Custom blocks](/world/custom-blocks/)
> "`data.remove(list, index?)` shifts following elements; its default is the last" — [Custom blocks](/world/custom-blocks/)
