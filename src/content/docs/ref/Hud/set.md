---
title: "hud:set"
description: "A value per id: a number is a fill, a string a label's words, true or false whether it shows"
---

Part of [`Hud`](/ref/Hud/).

```luau
hud:set(values: { [string]: number | string | boolean })
```

A value per id: a number is a fill, a string a label's words, true or false whether it shows. An unknown id is an error that lists the ids.

## Parameters

| Name     | Type                                          | Required |
| -------- | --------------------------------------------- | -------- |
| `values` | `{ [ string ]: number \| string \| boolean }` | yes      |

## Used in

> "hud:set{ hp = 0.7, hp_text = "14 / 20", level = "22" }" — [Layouts](/ui/screens/)
> "**The values.** An item with an `id` is live. `hud:set{}` takes a value per" — [Layouts](/ui/screens/)
