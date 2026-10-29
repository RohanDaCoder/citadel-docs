---
title: 'network.instances'
description: 'Everything this network runs: this experience''s own always-on servers (on the platform''s hub, the hubs), then its games started on demand'
---

Part of [`network`](/ref/network/).

```luau
network.instances(label: string ?) → ({BrowseEntry | NetworkInstance}?, string ?)
```

Everything this network runs: this experience's own always-on servers (on the platform's hub, the hubs), then its games started on demand. With `label`, only that mode's games.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `label` | `string` | no |

## Returns

- `({BrowseEntry | NetworkInstance}?, string ?)`

## Used in

> "- `network.instances(label?)` returns everything this network runs, as this experience sees it: first its own servers that run all the time, online and taking players, as `{id, name, state, players, region}` (on the platform's hub, the hubs), then the network's games started on demand, each the instance table below. With `label`, only that mode's games: `network.instances('4v4v4v4')`. `id` is what `player:connect` takes. Never another network's. It returns nil and why when Minefort did not answer." — [Network](/systems/network/)
> "**Events come to the default member's servers only.** Call `network.instances()` once at the start, then keep the list from `on_instance_start`, `on_instance_change` and `on_instance_stop`. An event can be lost. Call `network.instances()` again, once a minute at most, to repair the list." — [Network](/systems/network/)
> "with `network.browse`, and its hubs with `network.instances`, and asks the" — [Hub](/systems/hub/)
> "for _, h in network.instances() or {} do print(h.name, h.players) end" — [Hub](/systems/hub/)
