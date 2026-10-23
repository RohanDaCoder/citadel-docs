---
title: "time.every"
url: /docs/citadel/reference/time/every
---

# time.every

Calls `fn` every `seconds`, precise to 1 ms and never drifting; use it for music.

```
time.every(seconds: number, fn: () -> ()) → Connection
```


## Parameters


## Returns


## Used in
- [`local timer = time.every(0.1, function()`Guide: Parkour, a room each](/docs/citadel/guides/parkour-a-room-each)
- [`run's time. Ten times a second the action bar shows it. `time.every` gives`Guide: Parkour, a room each](/docs/citadel/guides/parkour-a-room-each)
- [`time.every(seconds, fn) -> connection -- precise (1 ms), never drifts; use it for music`Time and tweens](/docs/citadel/time-and-tweens)
- [`range; invalid values raise catchable errors. `time.every` remains a repeating`Modules and tasks](/docs/citadel/modules-and-tasks)
- [`- It covers `time.on_tick`, `time.every` and the survival events`Limits and reload](/docs/citadel/limits-and-reload)
- [`- A `time.every` timer that does not fit retains its place among due timers.`Limits and reload](/docs/citadel/limits-and-reload)
