---
title: "network.find"
description: "The instance to send players players to (1 unless set), or nil when none has room"
---

Part of [`network`](/ref/network/).

```luau
network.find(options: {label: string, players: number ?, party: (Player | string)?, start: {member: string, slots: number, data: any }?}) → (NetworkStarted ?, string ?)
```

The instance to send `players` players to (1 unless set), or nil when none has room. With `start`, one is started when none has room.

## Parameters

| Name      | Type                                                                                                                       | Required |
| --------- | -------------------------------------------------------------------------------------------------------------------------- | -------- |
| `options` | `{label: string , players: number ?, party: ( Player \| string )?, start: {member: string , slots: number , data: any }?}` | yes      |

## Returns

- `( NetworkStarted ?, string ?)`

## Used in

> "local arena, why = network.find{" — [Network](/systems/network/)
> "- `network.find{ label, players?, party?, start? }` returns `{id, state}` for the instance to send `players` players to, or nil when no instance has room." — [Network](/systems/network/)
