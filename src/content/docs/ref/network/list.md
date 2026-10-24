---
title: "network.list"
description: "The network's instances, or only those with label."
---

Part of [`network`](/ref/network/).

```luau
network.list(label: string ?) → ({ NetworkInstance }, string ?)
```

The network's instances, or only those with `label`.

## Parameters

| Name    | Type     | Required |
| ------- | -------- | -------- |
| `label` | `string` | no       |

## Returns

- `({ NetworkInstance }, string ?)`

## Used in

> "- `network.list(label?)` returns a list of the network's instances. Each one is the instance table below." — [Network](/systems/network/)
> "**Events come to the default member's servers only.** Call `network.list()` once at the start, then keep the list from `on_instance` and `on_gone`. An event can be lost. Call `network.list()` again, once a minute at most, to repair the list." — [Network](/systems/network/)
