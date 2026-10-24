---
title: "time.on_tick"
description: "Calls fn every tick, 20 times a second, with the tick number; keep it short."
---

Part of [`time`](/ref/time/).

```luau
time.on_tick(fn: (tick: number) -> ()) → Connection
```

Calls `fn` every tick, 20 times a second, with the tick number; keep it short.

## Parameters

| Name | Type                    | Required |
| ---- | ----------------------- | -------- |
| `fn` | `(tick: number ) -> ()` | yes      |

## Returns

- [`Connection`](/ref/Connection/)

## Used in

> "time.on_tick(function(tick) end) -> connection -- 20 times a second; keep it short" — [Time and tweens](/world/world-state/)
> "local conn = time.on_tick(function(tick)" — [Particles and lasers](/ui/fx/)
> "Use `time.on_tick` for work tied to world ticks. The actual wait may be longer" — [Modules and tasks](/concepts/runtime/)
> "- It covers `time.on_tick`, `time.every` and the survival events" — [Limits and reload](/systems/limits/)
> "- `time.on_tick` coalesces missed ticks: remaining listeners resume with the" — [Limits and reload](/systems/limits/)
