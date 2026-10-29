---
title: 'Socket type'
description: 'A WebSocket a pack opened with http.socket.'
---

A WebSocket a pack opened with `http.socket`.

## Functions

| Call | Purpose |
| --- | --- |
| [`send`](/ref/Socket/send/) | True while the connection is up. Terminal receive-queue overflow; nil otherwise. Queues text; false when closed or full. Messages over 1 MiB are errors. |
| [`cancel`](/ref/Socket/cancel/) | Closes the socket for good. |
