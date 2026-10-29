---
title: 'storage.set'
description: 'Saves a value under key in this pack''s storage.json; nil forgets it.'
---

Part of [`storage`](/ref/storage/).

```luau
storage.set(key: string, value: any)
```

Saves a value under `key` in this pack's storage.json; nil forgets it.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `key` | `string` | yes |
| `value` | `any` | yes |

## Used in

> "storage.set(key, p.data.coins)" — [Guide: Coin rush](/guides/guide-coin-rush/)
> "storage.set(key, p.data.coins)" — [Guide: Coin rush](/guides/guide-coin-rush/)
> "storage.set(key, t)" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
> "storage.set(key, t)" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
> "storage.set(key, (storage.get(key) or 0) + 1)" — [Scoreboard with a button](/guides/guide-scoreboard-with-a-button/)
> "- Each write is checked at the assignment by the `storage.set` rules. A" — [Custom blocks](/world/custom-blocks/)
