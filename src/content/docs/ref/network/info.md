---
title: "network.info"
description: "This server's network, by name, and the instance this pack runs on: id and the fields after it are nil on a server that is not one."
---

Part of [`network`](/ref/network/).

```luau
network.info() → ({network: string, id: string ?, member: string ?, label: string ?, slots: number ?, data: any }?, string ?)
```

This server's network, by name, and the instance this pack runs on: `id` and the fields after it are nil on a server that is not one.

## Returns

- `({network: string , id: string ?, member: string ?, label: string ?, slots: number ?, data: any }?, string ?)`

## Used in

> "- The name of the network sends the player to its default member. `network.info().network` is that name. `hub` is Minefort's hub." — [Body and movement](/players/movement/)
> "local me = network.info() -- `me.id` is nil on a server that is not an instance" — [Network](/systems/network/)
> "- `network.start{ member, label, slots, data? }` starts an instance of `member`. It returns `{id, state}` at once, with `state = "starting"`: the instance comes online later. `slots` is the number of players the instance takes. `data` is the pack's own value for the instance, read there with `network.info()`." — [Network](/systems/network/)
