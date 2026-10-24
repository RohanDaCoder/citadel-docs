---
title: "network.on_instance"
description: "Called when an instance starts or changes."
---

Part of [`network`](/ref/network/).

```luau
network.on_instance(handler: (instance: NetworkInstance) -> ()) → Connection
```

Called when an instance starts or changes.

## Parameters

| Name      | Type                                 | Required |
| --------- | ------------------------------------ | -------- |
| `handler` | `(instance: NetworkInstance ) -> ()` | yes      |

## Returns

- [`Connection`](/ref/Connection/)

## Used in

> "network.on_instance(function(instance)" — [Network](/systems/network/)
> "- `network.on_instance(fn)` calls `fn(instance)` when an instance starts or changes. It returns a connection." — [Network](/systems/network/)
