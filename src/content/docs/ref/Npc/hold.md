---
title: "npc:hold"
description: "Puts an item in the main hand; nil or false empties it"
---

Part of [`Npc`](/ref/Npc/).

```luau
npc:hold(item: (ItemSpec | false)?)
```

Puts an item in the main hand; nil or false empties it. An error on an unknown item.

## Parameters

| Name   | Type                    | Required |
| ------ | ----------------------- | -------- |
| `item` | `( ItemSpec \| false )` | no       |

## Used in

> "npc:hold{ item = "potion", color = colors.lime }" — [Items](/players/inventory/)
