---
title: 'storage.get'
description: 'Returns the value saved under key, or nil when there is none.'
---

Part of [`storage`](/ref/storage/).

```luau
storage.get(key: string) → any
```

Returns the value saved under `key`, or nil when there is none.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `key` | `string` | yes |

## Returns

- `any`

## Used in

> "local best = storage.get("best." .. player.uuid) or 0" — [Guide: Coin rush](/guides/guide-coin-rush/)
> "if p.data.coins > (storage.get(key) or 0) then" — [Guide: Coin rush](/guides/guide-coin-rush/)
> "local best = storage.get("best." .. player.uuid)" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
> "local best = storage.get(key)" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
> "local score = storage.get("taps." .. p.name) or 0" — [Scoreboard with a button](/guides/guide-scoreboard-with-a-button/)
> "storage.set(key, (storage.get(key) or 0) + 1)" — [Scoreboard with a button](/guides/guide-scoreboard-with-a-button/)
