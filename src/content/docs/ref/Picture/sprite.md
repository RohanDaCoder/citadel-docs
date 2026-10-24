---
title: "picture:sprite"
description: "Draws pixel art: each string a row, each character a dot scale pixels square (1 by default); a character with no ink is skipped."
---

Part of [`Picture`](/ref/Picture/).

```luau
picture:sprite(x: number, y: number, rows: { string }, inks: { [string]: Ink }, scale: number ?)
```

Draws pixel art: each string a row, each character a dot `scale` pixels square (1 by default); a character with no ink is skipped.

## Parameters

| Name    | Type                  | Required |
| ------- | --------------------- | -------- |
| `x`     | `number`              | yes      |
| `y`     | `number`              | yes      |
| `rows`  | `{ string }`          | yes      |
| `inks`  | `{ [ string ]: Ink }` | yes      |
| `scale` | `number`              | no       |
