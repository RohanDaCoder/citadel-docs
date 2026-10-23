---
title: "time.on_tick"
url: /docs/citadel/reference/time/on_tick
---

# time.on_tick

Calls `fn` every tick, 20 times a second, with the tick number; keep it short.

```
time.on_tick(fn: (tick: number) -> ()) → Connection
```


## Parameters


## Returns


## Used in
- [`time.on_tick(function(tick) end) -> connection -- 20 times a second; keep it short`Time and tweens](/docs/citadel/time-and-tweens)
- [`local conn = time.on_tick(function(tick)`Particles and lasers](/docs/citadel/particles-and-lasers)
- [`Use `time.on_tick` for work tied to world ticks. The actual wait may be longer`Modules and tasks](/docs/citadel/modules-and-tasks)
- [`- It covers `time.on_tick`, `time.every` and the survival events`Limits and reload](/docs/citadel/limits-and-reload)
- [`- `time.on_tick` coalesces missed ticks: remaining listeners resume with the`Limits and reload](/docs/citadel/limits-and-reload)
