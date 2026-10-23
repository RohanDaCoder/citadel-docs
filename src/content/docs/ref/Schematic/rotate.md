---
title: 'schematic:rotate'
description: 'The build''s width, height and length in blocks'
---

Part of [`Schematic`](/ref/Schematic/).

```luau
schematic:rotate(degrees: number) → Schematic
```

The build's width, height and length in blocks. The build's own lowest corner, which `origin` puts down; zero for a file. A new build turned clockwise seen from above (90, 180 or 270), states and all.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `degrees` | `number` | yes |

## Returns

- [`Schematic`](/ref/Schematic/)
