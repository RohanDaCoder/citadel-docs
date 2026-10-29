---
title: 'network.on_instance_change'
description: 'Called when an instance''s state, open, status or meta changes.'
---

Part of [`network`](/ref/network/).

```luau
network.on_instance_change(handler: (instance: NetworkInstance) -> ()) → Connection
```

Called when an instance's state, open, status or meta changes.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `handler` | `(instance: NetworkInstance) -> ()` | yes |

## Returns

- [`Connection`](/ref/Connection/)

## Used in

> "network.on_instance_change(function(instance)" — [Network](/systems/network/)
> "- `network.on_instance_change(fn)` calls `fn(instance)` when an instance's `state`, `open`, `status` or `meta` changes. It returns a connection." — [Network](/systems/network/)
