---
title: 'network.on_instance_start'
description: 'Called when an instance is first seen: started, or already running.'
---

Part of [`network`](/ref/network/).

```luau
network.on_instance_start(handler: (instance: NetworkInstance) -> ()) → Connection
```

Called when an instance is first seen: started, or already running.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `handler` | `(instance: NetworkInstance) -> ()` | yes |

## Returns

- [`Connection`](/ref/Connection/)

## Used in

> "- `network.on_instance_start(fn)` calls `fn(instance)` when an instance is first seen: started, or running when this server began to listen. It returns a connection." — [Network](/systems/network/)
