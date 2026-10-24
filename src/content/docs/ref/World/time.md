---
title: 'world.time'
description: 'Holds the sky at a time (ticks, or "sunrise", "day", "noon", "sunset", "night", "midnight"), or asks a function each tick, s seconds after the call'
---

Part of [`world`](/ref/World/).

```luau
world.time((at: number | TimeName | (s: number) -> number | TimeName) -> ()) → & (() -> number)
```

Holds the sky at a time (ticks, or "sunrise", "day", "noon", "sunset", "night", "midnight"), or asks a function each tick, `s` seconds after the call. With no argument: the time of day now, 0 to 23999.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `(at` | `number \| TimeName \| (s: number ) -> number \| TimeName ) -> ()` | yes |

## Returns

- `& (() -> number )`

## Used in

> "world.time("sunset")" — [Guide: Build a cottage](/guides/guide-build-a-cottage/)
> "`world.time("sunset")` holds the sky at sunset: low light makes the roof" — [Guide: Build a cottage](/guides/guide-build-a-cottage/)
> "world.time("day")                         -- the sky stays there; see "the time of day"" — [Blocks and terrain](/world/terrain-generation/)
> "world.time(function(s) return s * 20 end) -- asked each tick; s is seconds since this call" — [Blocks and terrain](/world/terrain-generation/)
