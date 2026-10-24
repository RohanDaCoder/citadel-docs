---
title: "socket:send"
description: "True while the connection is up"
---

Part of [`Socket`](/ref/Socket/).

```luau
socket:send(text: string) → boolean
```

True while the connection is up. Terminal receive-queue overflow; nil otherwise. Queues text; false when closed or full. Messages over 1 MiB are errors.

## Parameters

| Name   | Type     | Required |
| ------ | -------- | -------- |
| `text` | `string` | yes      |

## Returns

- `boolean`

## Used in

> "socket:send("hello") -- queues text; true if queued, false if closed or full" — [HTTP](/systems/http/)
