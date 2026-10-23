---
title: "http.socket"
url: /docs/citadel/reference/http/socket
---

# http.socket

Opens a WebSocket (`ws` or `wss`) and keeps it open: when the connection ends, the engine dials again. `on_message` gets each message on a tick.

```
http.socket(url: string, options: {headers: {[string]: string}?, on_message: (message: SocketMessage) -> ()}) → Socket
```


## Parameters


## Returns


## Used in
- [``http.socket` opens a WebSocket and keeps it open. Use it for what a server`HTTP](/docs/citadel/http)
- [`local socket = http.socket("wss://live.example.org/room/7", {`HTTP](/docs/citadel/http)
