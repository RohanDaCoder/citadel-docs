---
title: "storage.keys"
description: "Every key, sorted; with a prefix, only those that start with it."
---

Part of [`storage`](/ref/storage/).

```luau
storage.keys(prefix: string ?) → { string }
```

Every key, sorted; with a prefix, only those that start with it.

## Parameters

| Name     | Type     | Required |
| -------- | -------- | -------- |
| `prefix` | `string` | no       |

## Returns

- `{ string }`

## Used in

> "scores, with `storage.keys("best.")`." — [Guide: Coin rush](/guides/guide-coin-rush/)
> "`storage.keys("best.")`." — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
> "storage.keys("best.") -- every key with that prefix, sorted; storage.keys() is all of them" — [Storage](/systems/storage/)
