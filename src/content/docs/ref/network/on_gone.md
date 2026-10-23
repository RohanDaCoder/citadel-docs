---
title: 'network.on_gone'
description: 'Called with the id of an instance that is gone.'
---

Part of [`network`](/ref/network/).

```luau
network.on_gone(handler: (id: string) -> ()) → Connection
```

Called with the id of an instance that is gone.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `handler` | `(id: string ) -> ()` | yes |

## Returns

- [`Connection`](/ref/Connection/)

## Used in

> "network.on_gone(function(id) waiting[id] = nil end)" — [Network](/systems/network/)
> "- `network.on_gone(fn)` calls `fn(id)` when an instance is gone. It returns a connection." — [Network](/systems/network/)
