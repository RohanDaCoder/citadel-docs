---
title: 'time.now'
description: 'Seconds since the pack started.'
---

Part of [`time`](/ref/time/).

```luau
time.now() → number
```

Seconds since the pack started.

## Returns

- `number`

## Used in

> "local started = time.now()" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
> "player.ui.actionbar(seconds(time.now() - started), "yellow")" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
> "time.now()                           -- seconds since the pack started" — [Time and tweens](/world/world-state/)
> "`time.now()` starts again at zero when the pack does. Use it for what" — [Time and tweens](/world/world-state/)
> "-- a rainbow, one cycle a second: letter, its number i of n, and t = time.now()" — [Text formatting](/ui/ui-basics/)
> "-- the letters appear one after another, `rate` a second from `from = time.now()`" — [Text formatting](/ui/ui-basics/)
