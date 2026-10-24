---
title: 'time.every'
description: 'Calls fn every seconds, precise to 1 ms and never drifting; use it for music.'
---

Part of [`time`](/ref/time/).

```luau
time.every(seconds: number, fn: () -> ()) → Connection
```

Calls `fn` every `seconds`, precise to 1 ms and never drifting; use it for music.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `seconds` | `number` | yes |
| `fn` | `() -> ()` | yes |

## Returns

- [`Connection`](/ref/Connection/)

## Used in

> "local timer = time.every(0.1, function()" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
> "run's time. Ten times a second the action bar shows it. `time.every` gives" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
> "time.every(seconds, fn) -> connection            -- precise (1 ms), never drifts; use it for music" — [Time and tweens](/world/world-state/)
> "range; invalid values raise catchable errors. `time.every` remains a repeating" — [Modules and tasks](/concepts/runtime/)
> "- It covers `time.on_tick`, `time.every` and the survival events" — [Limits and reload](/systems/limits/)
> "- A `time.every` timer that does not fit retains its place among due timers." — [Limits and reload](/systems/limits/)
