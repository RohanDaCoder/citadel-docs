---
title: "world.time"
url: /docs/citadel/reference/World/time
---

# world.time

Holds the sky at a time (ticks, or "sunrise", "day", "noon", "sunset", "night", "midnight"), or asks a function each tick, `s` seconds after the call. With no argument: the time of day now, 0 to 23999.

```
world.time((at: number | TimeName | (s: number) -> number | TimeName) -> ()) →  & (() -> number)
```


## Parameters


## Returns


## Used in
- [`world.time("sunset")`Guide: Build a cottage](/docs/citadel/guides/build-a-cottage)
- [``world.time("sunset")` holds the sky at sunset: low light makes the roof`Guide: Build a cottage](/docs/citadel/guides/build-a-cottage)
- [`world.time("day") -- the sky stays there; see "the time of day"`Blocks and terrain](/docs/citadel/blocks-and-terrain)
- [`world.time(function(s) return s * 20 end) -- asked each tick; s is seconds since this call`Blocks and terrain](/docs/citadel/blocks-and-terrain)
