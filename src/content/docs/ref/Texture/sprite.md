---
title: "texture:sprite"
description: "Draws pixel art from rows of characters, each character painted with its ink, as on a screen."
---

Part of [`Texture`](/ref/Texture/).

```luau
texture:sprite(x: number, y: number, rows: { string }, inks: { [string]: Ink }, scale: number ?)
```

Draws pixel art from rows of characters, each character painted with its ink, as on a screen.

## Parameters

| Name    | Type                  | Required |
| ------- | --------------------- | -------- |
| `x`     | `number`              | yes      |
| `y`     | `number`              | yes      |
| `rows`  | `{ string }`          | yes      |
| `inks`  | `{ [ string ]: Ink }` | yes      |
| `scale` | `number`              | no       |
