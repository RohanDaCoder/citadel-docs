---
title: "http global"
description: "HTTP requests from the pack, with caching."
---

HTTP requests from the pack, with caching.

Part of the [Storage](/systems/storage/) article.

## Functions

| Call                          | Purpose                                                                                                                                          |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`get`](/ref/http/get/)       | GET a URL. `cache` is the seconds a 200 answer is kept on disk; `timeout` is 1 to 60 seconds, 15 by default.                                     |
| [`socket`](/ref/http/socket/) | Opens a WebSocket (`ws` or `wss`) and keeps it open: when the connection ends, the engine dials again. `on_message` gets each message on a tick. |
