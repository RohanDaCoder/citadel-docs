---
title: 'network.online'
description: 'How many play on this network (everyone on Minefort on the platform''s hub), or in one mode''s games'
---

Part of [`network`](/ref/network/).

```luau
network.online(label: string ?) → (number ?, string ?)
```

How many play on this network (everyone on Minefort on the platform's hub), or in one mode's games. An answer is kept for 5 seconds.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `label` | `string` | no |

## Returns

- `(number ?, string ?)`

## Used in

> "- `network.online(label?)` returns how many play on this network: on the platform's hub, everyone on Minefort; on any other network, its members and their instances. With `label`, only the players in that mode's games, every region's. An answer is kept for 5 seconds, so a scoreboard can ask on every redraw. It returns nil and why when Minefort did not answer." — [Network](/systems/network/)
> "count with `network.online`. On a server that is not a hub, every" — [Hub](/systems/hub/)
> "print(network.online())" — [Hub](/systems/hub/)
