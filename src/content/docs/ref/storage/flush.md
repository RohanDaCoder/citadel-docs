---
title: "storage.flush"
description: "Yields until saved; raises an error on failure"
---

Part of [`storage`](/ref/storage/).

```luau
storage.flush()
```

Yields until saved; raises an error on failure. After initialization only.

## Used in

> "failure remains visible and is retried. `storage.flush()` yields until the" — [Storage](/systems/storage/)
> "- Writes to shared stores, purchase prompts/acks and `storage.flush` belong" — [Limits and reload](/systems/limits/)
