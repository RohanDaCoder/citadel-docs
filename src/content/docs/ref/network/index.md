---
title: 'network global'
description: 'WebSockets out and listening sockets, for multiplayer-scale IO.'
---

WebSockets out and listening sockets, for multiplayer-scale IO.

Part of the [Storage](/systems/storage/) article.

## Functions

| Call | Purpose |
| --- | --- |
| [`start`](/ref/network/start/) | Starts an instance of `member`. Answers at once; it is online later. |
| [`find`](/ref/network/find/) | The instance to send `players` players to (1 unless set), or nil when none has room. With `start`, one is started when none has room. |
| [`stop`](/ref/network/stop/) | Stops an instance of this network. |
| [`info`](/ref/network/info/) | This server's network, by name, and the instance this pack runs on: `id` and the fields after it are nil on a server that is not one. |
| [`status`](/ref/network/status/) | Says where this instance is. At most one a second is sent: the first at once, then the last of those that came after. |
| [`on_instance_start`](/ref/network/on_instance_start/) | Called when an instance is first seen: started, or already running. |
| [`on_instance_change`](/ref/network/on_instance_change/) | Called when an instance's state, open, status or meta changes. |
| [`on_instance_stop`](/ref/network/on_instance_stop/) | Called with the id of an instance that is gone. |
| [`online`](/ref/network/online/) | How many play on this network (everyone on Minefort on the platform's hub), or in one mode's games. An answer is kept for 5 seconds. |
| [`browse`](/ref/network/browse/) | The platform's hub finding every network, in the order to show them. nil and why on a refusal, and anywhere but that hub. One page of 6 rows (page from 1), and how many there are in all; nil and why on a refusal. |
| [`instances`](/ref/network/instances/) | Everything this network runs: this experience's own always-on servers (on the platform's hub, the hubs), then its games started on demand. With `label`, only that mode's games. |
