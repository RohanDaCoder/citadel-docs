---
title: "data.insert"
description: "Insert into a nested data list; omitted index appends."
---

Part of [`data`](/ref/data/).

```luau
data.insert((list: DataView, value: any) -> ()) → & ((list: DataView, index: number, value: any) -> ())
```

Insert into a nested data list; omitted index appends.

## Parameters

| Name    | Type                            | Required |
| ------- | ------------------------------- | -------- |
| `(list` | `DataView , value: any ) -> ()` | yes      |

## Returns

- `& ((list: DataView , index: number , value: any ) -> ())`

## Used in

> "data.insert(e.data.history, { score = 12 })" — [Custom blocks](/world/custom-blocks/)
> "append, or use `data.insert(list, value)` / `data.insert(list, index, value)`." — [Custom blocks](/world/custom-blocks/)
