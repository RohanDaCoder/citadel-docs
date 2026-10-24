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
| [`list`](/ref/network/list/) | The network's instances, or only those with `label`. |
| [`stop`](/ref/network/stop/) | Stops an instance of this network. |
| [`info`](/ref/network/info/) | This server's network, by name, and the instance this pack runs on: `id` and the fields after it are nil on a server that is not one. |
| [`status`](/ref/network/status/) | Says where this instance is. At most one a second is sent: the first at once, then the last of those that came after. |
| [`on_instance`](/ref/network/on_instance/) | Called when an instance starts or changes. |
| [`on_gone`](/ref/network/on_gone/) | Called with the id of an instance that is gone. |
