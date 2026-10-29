---
title: 'http.socket'
description: 'Opens a WebSocket (ws or wss) and keeps it open: when the connection ends, the engine dials again'
---

Part of [`http`](/ref/http/).

```luau
http.socket(url: string, options: {headers: {[string]: string }?, on_message: (message: SocketMessage) -> ()}) → Socket
```

Opens a WebSocket (`ws` or `wss`) and keeps it open: when the connection ends, the engine dials again. `on_message` gets each message on a tick.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `url` | `string` | yes |
| `options` | `{headers: {[ string ]: string }?, on_message: (message: SocketMessage ) -> ()}` | yes |

## Returns

- [`Socket`](/ref/Socket/)

## Used in

> "`http.socket` opens a WebSocket and keeps it open. Use it for what a server" — [HTTP](/systems/http/)
> "local socket = http.socket("wss://live.example.org/room/7", {" — [HTTP](/systems/http/)
