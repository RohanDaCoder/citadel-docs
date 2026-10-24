---
title: "texture:noise"
description: "Paints each pixel in the area one of the colours at random, as for stone, bark or grain."
---

Part of [`Texture`](/ref/Texture/).

```luau
texture:noise(x: number, y: number, w: number, h: number, colors: { Ink }, seed: number ?)
```

Paints each pixel in the area one of the colours at random, as for stone, bark or grain.

## Parameters

| Name     | Type      | Required |
| -------- | --------- | -------- |
| `x`      | `number`  | yes      |
| `y`      | `number`  | yes      |
| `w`      | `number`  | yes      |
| `h`      | `number`  | yes      |
| `colors` | `{ Ink }` | yes      |
| `seed`   | `number`  | no       |
