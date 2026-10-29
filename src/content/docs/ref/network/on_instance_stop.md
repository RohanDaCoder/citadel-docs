---
title: 'network.on_instance_stop'
description: 'Called with the id of an instance that is gone.'
---

Part of [`network`](/ref/network/).

```luau
network.on_instance_stop(handler: (id: string) -> ()) → Connection
```

Called with the id of an instance that is gone.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `handler` | `(id: string) -> ()` | yes |

## Returns

- [`Connection`](/ref/Connection/)

## Used in

> "network.on_instance_stop(function(id) waiting[id] = nil end)" — [Network](/systems/network/)
> "- `network.on_instance_stop(fn)` calls `fn(id)` when an instance is gone. It returns a connection." — [Network](/systems/network/)
