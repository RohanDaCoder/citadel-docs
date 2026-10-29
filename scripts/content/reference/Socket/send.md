---
title: "socket:send"
url: /docs/citadel/reference/Socket/send
---

# socket:send

True while the connection is up. Terminal receive-queue overflow; nil otherwise. Queues text; false when closed or full. Messages over 1 MiB are errors.

```
socket:send(text: string) → boolean
```


## Parameters


## Returns


## Used in
- [`socket:send("hello") -- queues text; true if queued, false if closed or full`HTTP](/docs/citadel/http)
