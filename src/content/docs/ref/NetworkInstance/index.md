---
title: 'NetworkInstance type'
description: 'An instance of a member: a server the network started for itself.'
---

An instance of a member: a server the network started for itself.

## Fields

| Field | Purpose |
| --- | --- |
| [`networkInstance.id: string`](/ref/NetworkInstance/id/) | The instance's name. `player:connect` takes it. |
| [`networkInstance.member: string`](/ref/NetworkInstance/member/) |  |
| [`networkInstance.label: string`](/ref/NetworkInstance/label/) |  |
| [`networkInstance.state: string`](/ref/NetworkInstance/state/) | "starting", then "online", then "stopping". |
| [`networkInstance.open: number ?`](/ref/NetworkInstance/open/) | The number of players it takes now, as it said with `network.status`. |
| [`networkInstance.status: string ?`](/ref/NetworkInstance/status/) | The instance's own word. |
| [`networkInstance.players: number ?`](/ref/NetworkInstance/players/) | The number of players on it. |
| [`networkInstance.meta: any`](/ref/NetworkInstance/meta/) | The instance's own value. |
