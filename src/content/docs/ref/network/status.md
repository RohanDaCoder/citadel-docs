---
title: 'network.status'
description: 'Says where this instance is'
---

Part of [`network`](/ref/network/).

```luau
network.status(options: {open: number, status: string ?, meta: any })
```

Says where this instance is. At most one a second is sent: the first at once, then the last of those that came after.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `options` | `{open: number , status: string ?, meta: any }` | yes |

## Used in

> "if me and me.id then network.status{ open = math.max(0, me.slots - #players.list()), status = "waiting" } end" — [Network](/systems/network/)
> "-- When the round starts: network.status{ open = 0, status = "playing" }" — [Network](/systems/network/)
