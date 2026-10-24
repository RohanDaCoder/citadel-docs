---
title: "display:animate"
description: "Makes one tweened change of place, scale, rotation or text over duration seconds (0.5 by default), played by the client."
---

Part of [`Display`](/ref/Display/).

```luau
display:animate(opts: { at: Vec3 ?, scale: (Vec3 | number)?, rotation: Orientation ?, text: Text ?, color: Ink ?, background: (Ink | false)?, line_width: number ?, shadow: boolean ?, duration: number ?, })
```

Makes one tweened change of place, scale, rotation or text over `duration` seconds (0.5 by default), played by the client.

## Parameters

| Name   | Type                                                                                                                                                                                           | Required |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| `opts` | `{ at: Vec3 ?, scale: ( Vec3 \| number )?, rotation: Orientation ?, text: Text ?, color: Ink ?, background: ( Ink \| false )?, line_width: number ?, shadow: boolean ?, duration: number ?, }` | yes      |

## Used in

> "Use `display:animate{..., duration = seconds}` for an authored display transition," — [Displays](/ui/displays/)
