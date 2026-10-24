---
title: "picture:gradient"
description: 'Fills a box that fades from from to to, top to bottom; "across" runs it left to right.'
---

Part of [`Picture`](/ref/Picture/).

```luau
picture:gradient(x: number, y: number, w: number, h: number, from: Ink, to: Ink, across: string ?)
```

Fills a box that fades from `from` to `to`, top to bottom; `"across"` runs it left to right.

## Parameters

| Name     | Type               | Required |
| -------- | ------------------ | -------- |
| `x`      | `number`           | yes      |
| `y`      | `number`           | yes      |
| `w`      | `number`           | yes      |
| `h`      | `number`           | yes      |
| `from`   | [`Ink`](/ref/Ink/) | yes      |
| `to`     | [`Ink`](/ref/Ink/) | yes      |
| `across` | `string`           | no       |
