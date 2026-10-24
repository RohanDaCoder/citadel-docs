---
title: "data.copy"
description: "A detached JSON snapshot as ordinary Lua values/tables."
---

Part of [`data`](/ref/data/).

```luau
data.copy(value: any) → any
```

A detached JSON snapshot as ordinary Lua values/tables.

## Parameters

| Name    | Type  | Required |
| ------- | ----- | -------- |
| `value` | `any` | yes      |

## Returns

- `any`

## Used in

> "local snapshot = data.copy(e.data) -- an ordinary, detached Lua table" — [Custom blocks](/world/custom-blocks/)
> "are userdata, so use `data.copy(view)` before ordinary `table.*`, `pairs`, or" — [Custom blocks](/world/custom-blocks/)
